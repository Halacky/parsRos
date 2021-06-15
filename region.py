import selenium
from selenium import webdriver
import time

from selenium.common.exceptions import StaleElementReferenceException

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup


class Region:

    def __init__(self,dataBlock):
        self.dataBlock = dataBlock

    #Здесь распарсиваем данные из столбца
    def extractInfo(self):
        regionInfoArray = []
        time.sleep(1)
        for result in self.dataBlock:
            try:
                regionInfo = result.find_element_by_css_selector("div.expanding-box_content").text
                regionInfoArray.append(regionInfo)
            except StaleElementReferenceException:
                try:
                    regionInfo = result.find_element_by_css_selector("div.expanding-box_content").text
                    regionInfoArray.append(regionInfo)
                except StaleElementReferenceException:
                    regionInfoArray.append("")


        return regionInfoArray


