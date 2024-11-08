import pandas as pd
from src.headerNames import HeaderNames
from src.config import Config


def readSheet(filePath, nrows=None):
    sheet = pd.read_excel(filePath, index_col=HeaderNames.id_s, nrows=nrows)
    # if there is a "Downloaded" field in the loaded sheet, set update mode
    if HeaderNames.downloaded in sheet:
        Config.updateMode = True
    return sheet


def writeSheet(sheet):
    filePath = Config.inputFile
    # if in update mode, input file is overwritten
    if not Config.updateMode:
        filePath.replace(".xlsx", "_Downloaded.xlsx")
    with pd.ExcelWriter(filePath) as writer:
        sheet.to_excel(writer)
