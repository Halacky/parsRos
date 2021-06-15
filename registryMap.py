import selenium
from selenium import webdriver
import os
import screenShot

class Map:

    def __init__(self, webDriver, registryNumber):
        self.driver = webDriver
        self.registryNumber = str(registryNumber)


    def getScreenShot(self, registryNumber):
        registryNumber = registryNumber.replace(":","")
        output_path, output_picture_path = self.getSavePath(registryNumber)
        try:
            os.mkdir(output_path)
        except OSError:
            pass

        registryNumber = self.registryNumber.replace(":", "")
        print(output_path)
        print(output_picture_path)

        self.driver.save_screenshot(output_picture_path)
        return self.cropScreenShot(output_picture_path),output_path

    def getSavePath(self, registryNumber):
        output_path = 'output_pics/' + registryNumber
        output_picture_path = output_path + '/' + registryNumber +'.png'
        return  output_path,output_picture_path


    def cropScreenShot(self, imageLink):
        imageShot = screenShot.Image(imageLink)
        return imageShot.cropImage()



