import src.excelIO as eIO
import src.logger as logger
from src.config import Config
from pathlib import Path
import sys
from src.pdfDownload import processSheet_mt

usageString = """\
usage: python downloadPdfs.py [-l | -p | -v] [threads=] [inputfile.xlsx [outputfolderpath]]

Reads the inputfile.xlsx (default "GRI_2017_2020.xlsx") and downloads the pdf files listed to the outputfolderpath (default /files/). Also outputs an augmented inputfile_Downloaded.xlsx, which lists the results of downloads.
inputfile.xlsx must be specified in order to also specify outputfolder
Use argument "threads=[int]" to specify the number of threads. Otherwise python will decide.
Use argument "nrows=[int]" to limit the number of rows processed.
    options:
        -l logs error messages in ./logs/error.log. Useful for understanding why files weren't downloaded
        -p records the performance and time of execution and appends it to ./logs/performance.log
        -v prints verbose error/warning messages
        -h, --help prints this message
"""


def main():
    parseArgs()
    if Config.logPerformance:
        performance = logger.Performance()
        performance.start()
    try:
        success = True
        sheet = eIO.readSheet(Config.inputFile, nrows=Config.nrows)
        sheet = processSheet_mt(sheet)
        eIO.writeSheet(sheet)
    except Exception as e:
        print(e)
        success = False
    finally:
        if Config.logPerformance:
            if performance is not None:
                performance.stop(write=success)
            else:
                print("performance error")
        if Config.logErrors:
            logger.writeErrs()


def parseArgs():
    for arg in sys.argv[1:]:
        if arg[0] == "-":  # Starts with "-"? is then treatet as option
            handleOptions(arg)
        else:
            handleOptionalArgs(arg)
    if Config.inputFile is None:
        Config.inputFile = Config.defaultInputFile
    if Config.outputFolder is None:
        Config.outputFolder = Config.defaultOutputFolder


def handleOptionalArgs(arg):
    if "=" in arg:
        key, val = arg.split("=")
        match key:
            case "threads":
                Config.threads = int(val)
            case "nrows":
                Config.nrows = int(val)
    else:  # path inputs
        print(arg)
        if Config.inputFile is None:
            if arg.endswith(".xlsx"):
                Config.inputFile = arg
            else:
                raise Exception(
                    f"expected argument to end with '.xlsx': {arg}")
        elif Config.outputFolder is None:
            Config.outputFolder = arg
        else:  # ignore are
            print(f"ignored argument {arg}")


def handleOptions(arg):
    match arg:
        case "-l":
            Config.logErrors = True
        case "-p":
            Config.logPerformance = True
        case "-v":
            Config.verbose = True
        case "-h":
            print(usageString)
            sys.exit()
        case "--help":
            print(usageString)
            sys.exit()


if __name__ == "__main__":
    main()
