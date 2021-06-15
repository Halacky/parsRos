import pandas as pd

class ExcelDocument:

    def __init__(self, pathToExcel):
        self.pathToExcel = pathToExcel

    def readExcel(self):
        return pd.read_excel(self.pathToExcel)


