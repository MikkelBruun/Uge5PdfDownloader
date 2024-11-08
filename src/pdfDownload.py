import requests
import os
import src.logger as logger
from src.config import Config
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
from src.headerNames import HeaderNames
from pathlib import Path
lock = Lock()


# processSheet takes a loaded sheet, and attempts to download the linked pdf documents
# First tries field "Pdf_URL" then "Report Html Address" as a backup
# Notes whether the download is successful in a new column in hte sheet
# Returns the updated sheet


# def processSheet(sheet):
#     # process sequentially
#     os.makedirs("files", exist_ok=True)
#     sheet["Downloaded"] = False
#     total = len(sheet)
#     finished, failures = 0, 0
#     for tup in sheet[[HeaderNames.url1_s, HeaderNames.url2_s]].itertuples():
#         result = _mapRow(tup)
#         BRnum, _, _ = tup
#         sheet.loc[BRnum, "Downloaded"] = result
#         finished += 1
#     print(f"Downloaded {total-failures}/{total}")
#     return sheet


def processSheet_mt(sheet, threads=None):
    # process concurrently
    os.makedirs(Config.outputFolder, exist_ok=True)
    executor = ThreadPoolExecutor(threads)
    if Config.updateMode:
        results = executor.map(
            _mapRowUpdate, sheet[[HeaderNames.url1_s, HeaderNames.url2_s, HeaderNames.downloaded]].itertuples())
    else:
        results = executor.map(
            _mapRow, sheet[[HeaderNames.url1_s, HeaderNames.url2_s]].itertuples())
    sheet["Downloaded"] = list(results)
    return sheet


# local function wrapper
def logErr(msg):
    logger.logErr("[pdfDownload] "+msg)


def _mapRowUpdate(tup):
    BRnum, url1, url2, download = tup
    if download == "Success":
        return download
    else:
        return _mapRow((BRnum, url1, url2))


def _mapRow(tup):
    BRnum, url1, url2 = tup
    filePath = Config.outputFolder.joinpath(f"{BRnum}.pdf")
    success = download(url1, filePath)
    if not success:
        success = download(url2, filePath)
    if (False):  # Not used, as it impacts performance
        with lock:
            logger.incrementProgress_s()
    elif Config.verbose:
        print(f"{BRnum} {success}")
    return "Success" if success else "Error"


def download(url, filePath: Path,) -> bool:
    # Attempts to download a file from a given url
    # Writes the file to filePath
    # Returns a bool depending on whether the file was successfully downloaded

    # Used to identify problematic entries in the log file
    _errId = filePath.parts[len(filePath.parts)-1]
    try:
        if (url is None or url == "" or str(url) == "nan"):
            logErr(f"{_errId} Invalid url: {url}")
            return False
        else:
            try:
                res = requests.get(url, timeout=1)
            except Exception as e:
                logErr(f"{_errId} {e}")
                return False
            if (res.status_code != 200):
                logErr(f"{_errId} response code: {res.status_code}")
                return False
            if (res.headers["content-type"] != "application/pdf"):
                logErr(f"{_errId} Expected content-type 'application/pdf' but recieved: {
                       (res.headers["content-type"])}")
                return False
            with filePath.open("wb") as file:
                try:
                    file.write(res.content)
                except Exception as e:
                    if Config.verbose:
                        print(e)
                    return False
                else:
                    return True
    except Exception as e:
        logErr(f"{_errId} Unexpected error: {e}")
        return False
