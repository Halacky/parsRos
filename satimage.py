from rosreestr2coord import Area

class regionSat:

     def __init__(self, regionNumber):
         self.regionNumber = regionNumber

     def getArea(self):
         area = Area(self.regionNumber)
