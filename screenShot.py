import cv2

class Image:
    def __init__(self, imageLink):
        self.imageLink = imageLink


    def readImage(self):
        try:
            imgRead = cv2.imread(self.imageLink)
            return imgRead
        except Exception:
            print(Exception)
            return False

    def cropImage(self):
        image = self.readImage()
        imageHeight, imageWidth, channels = image.shape
        # Обрезаем половину картинки, левая часть нафиг не нужна и перезаписываем ее в ту же папку
        targetWidth = int(imageWidth / 3)
        croppedImage = image[0: 0 + imageHeight, targetWidth: targetWidth + targetWidth*2]
        cv2.imwrite(self.imageLink, croppedImage)
        return croppedImage

