import cv2
import numpy as np


class Filter:

    def __init__(self, croppedImage, hsvMinTop, hsvMinMiddle, hsvMinLow, hsvMaxTop, hsvMaxMiddle, hsvMaxLow, filterColorName, outputPath):
        self.croppedImage = croppedImage
        self.hsvMinTop = hsvMinTop
        self.hsvMinMiddle = hsvMinMiddle
        self.hsvMinLow = hsvMinLow
        self.hsvMaxTop = hsvMaxTop
        self.hsvMaxMiddle = hsvMaxMiddle
        self.hsvMaxLow = hsvMaxLow
        self.filterColorName = filterColorName
        self.outputPath = outputPath
        #self.hsv_min = hsv_min
        #self.hsv_max = hsv_max

    def getContour(self):
        contourCoordinatesArray, contourAreaValue = self.getContourCoordinates()
        labelRectangle = cv2.boundingRect(contourCoordinatesArray)
        x, y, w, h = labelRectangle
        ##TODO что-то с кропнутой фоткой, после фильтра она вся черная + на 46 строке выдает ошибку мол параметров не хватает 
        croped = self.croppedImage[y:y + h, x:x + w].copy()
        
        ## (2) make mask
        contourCoordinatesArray = contourCoordinatesArray - contourCoordinatesArray.min(axis=0)

        mask = np.zeros(croped.shape[:2], np.uint8)
        cv2.drawContours(mask, [contourCoordinatesArray], -1, (255, 255, 255), -1, cv2.LINE_AA)
        contour = cv2.bitwise_and(croped, croped, mask=mask)
        cv2.imwrite(self.outputPath + '/' + '{}.png'.format(self.filterColorName), contour)
        return contour, contourAreaValue

    def getContourCoordinates(self):
        """
        Метод возвращает координаты углов выделенной области и ее площадь.
        :return: array, int
        :rtype:
        """
        # Получаем контур фигуры, из  которой получим координаты хуйни
        contours, hierarchy = cv2.findContours(
            image=self.filterColor(),
            mode=cv2.RETR_TREE,
            method=cv2.CHAIN_APPROX_SIMPLE)

        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        contoursArray = contours[0]
        #Получаем из контура необходимые точки
        leftPoint = np.array(contoursArray[contoursArray[:, :, 0].argmin()][0])
        rightPoint = np.array(contoursArray[contoursArray[:, :, 0].argmax()][0])
        topPoint = np.array(contoursArray[contoursArray[:, :, 1].argmin()][0])
        bottomPoint = np.array(contoursArray[contoursArray[:, :, 1].argmax()][0])

        coordinatesArray = np.array([leftPoint, topPoint, rightPoint, bottomPoint])

        return coordinatesArray, cv2.contourArea(contours[0])

    def filterColor(self):
        """
        Функция фильтрует по желтому цвету
        :return: numpy.array
        :rtype:
        """
        # Накладываем фильтр и убираем шум
        imgBlurred = cv2.bilateralFilter(self.croppedImage, d=7, sigmaSpace=75, sigmaColor=75)
        # Фильтр по желтой области

        hsv_min = np.array((self.hsvMinTop, self.hsvMinMiddle, self.hsvMinLow), np.uint8)
        hsv_max = np.array((self.hsvMaxTop, self.hsvMaxMiddle, self.hsvMaxLow), np.uint8)

        # Меняем BGR на HSV по фильтру
        hsv = cv2.cvtColor(imgBlurred, cv2.COLOR_BGR2HSV)
        thresh = cv2.inRange(hsv, hsv_min, hsv_max)
        cv2.imwrite('2.png', thresh)
        # Вовзращаем картинку с наложенным фильтром
        return thresh
