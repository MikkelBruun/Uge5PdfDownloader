import pathlib


class Config:
    defaultInputFile = "GRI_2017_2020.xlsx"
    inputFile = None
    defaultOutputFolder = pathlib.Path("./files")
    outputFolder = None
    logErrors = True
    logPerformance = True
    verbose = False
    threads = None
    nrows = 20  # TEMP
    updateMode = False

    def prettyprint():
        print(f"""\
inputfile = {Config.inputFile}
outputfolder = {Config.outputFolder}
logerrors = {Config.logErrors}
logperformance = {Config.logPerformance}
verbose = {Config.verbose}
threads = {Config.threads}
nrows = {Config.nrows}""")
