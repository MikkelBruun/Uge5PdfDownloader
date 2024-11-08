import os
import time
from src.config import Config
ERRS = []


def logErr(msg):
    # Errors logged will be written to logs/error.log at the end of the program
    global ERRS
    ERRS.append(msg+'\n')
    if Config.verbose:
        print(msg)


def writeErrs(filePath="logs/error.log"):
    global ERRS
    os.makedirs("logs", exist_ok=True)
    with open(filePath, "w") as F:
        F.writelines(ERRS)


class Performance:
    def __init__(self, logFilePath="logs/performance.log"):
        self.t1 = None
        self.t2 = None
        self.logFilePath = logFilePath

    def start(self):
        self.t1 = time.perf_counter()

    def stop(self, write=True):
        self.t2 = time.perf_counter()
        if write:
            self.writeLog()

    def _getLogEntry(self):
        items = Config.nrows if Config.nrows else "all"
        return (f"{time.strftime("%c", time.localtime())}    " +
                f"| maxthreads={Config.threads}  items={items}    time={self.t2-self.t1}\n")

    def writeLog(self):
        if (self.t1 is not None and self.t2 is not None):
            os.makedirs("logs", exist_ok=True)
            with open(self.logFilePath, "a") as log:
                log.write(self._getLogEntry())
