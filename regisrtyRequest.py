import selenium
from selenium import webdriver
import time
from selenium.common.exceptions import TimeoutException

import region
import re

class registryRequest:

    URL = 'https://pkk.rosreestr.ru/'

    def __init__(self, registryNumber):
        self.registryNumber = registryNumber

    def createConnection(self):
        DRIVER = webdriver.Chrome('D:\Downloads\chromedriver_win32\chromedriver.exe')
        DRIVER.implicitly_wait(20)
        # Ждем 10 секунд, если не прогрузилось, возвращаем что сайт не работает
        DRIVER.set_page_load_timeout(20)
        try:
            return DRIVER
        except:
            return 0

    def loadPage(self):
        pageDriver = self.createConnection()
        #Выставляем параметры окна, чтобы удобнее вытаскивать скриншот
        pageDriver.set_window_position(0, 0)
        pageDriver.set_window_size(1920, 1080)
        try:
             pageDriver.get(self.URL)
        except TimeoutException:
            return 0

        if(pageDriver != 0):
            dropTutorial = pageDriver.find_element_by_class_name('tutorial-button-outline')
            if(type(dropTutorial) != None):
                pageDriver.execute_script("arguments[0].click();", dropTutorial)
            
            ##Закрытие окна с уведомлением (если оно есть)
            dropNotification = pageDriver.find_element_by_class_name('feature-notification')
            if(type(dropNotification) != None):
                pageDriver.find_element_by_class_name('close-icon-container').click()
            
            #Активируем подсветку областей
            # setLayersInfo = pageDriver.find_element_by_xpath('//*[@id="map-area"]/div[2]/div[1]/div[1]')
            # setLayersInfo.click()
            # time.sleep(0.5)
            # LayerCheckbox = pageDriver.find_element_by_xpath('//*[@id="map-area"]/div[2]/div[1]/div[1]/div/div/div[1]/div[6]/div/div[1]/div/div[2]')
            # time.sleep(0.5)
            # LayerCheckbox.click()
            # setLayersInfo.click()

            registryNumberInputForm = pageDriver.find_element_by_css_selector("input.type-ahead-select")
            time.sleep(3)

            #Активируем режим с зонами особого пользования
            pageDriver.find_element_by_class_name("type").click()
            time.sleep(3)
            tps = {1: "Участки", 2: "ОКС", 3: "Комплксы", 
                   4: "Проекты ЗУ", 5: "Жилищное строительство", 
                   6: "Адреса", 7: "Кварталы", 8: "Районы", 9: "Округа",
                   10: "ЗОУИТ", 11: "Зоны и территории", 12: "Территориальные зоны", 
                   13: "Красные линии", 14: "Границы", 15: "Негативные границы", 
                   16: "Усолье-Сибирское"}
            ##TODO Переписать строку поиска (сделать словарь со всеми возможными значениями из списка)
            pageDriver.find_element_by_xpath('//div[contains(text(),"{}")]'.format(tps[2])).click()
            time.sleep(3)
        
            #Вводим кадастровый в форму и инициализируем ее
            #registryNumberInputForm.clear()
            registryNumberInputForm.send_keys(self.registryNumber)
            time.sleep(3)
            pageDriver.find_element_by_class_name("button-container-search").click()
            # time.sleep(3)
            # pageDriver.find_element_by_class_name("button-container-search").click()
            # time.sleep(3)
            # pageDriver.find_element_by_class_name("button-container-search").click()
            # time.sleep(3)
            # pageDriver.find_element_by_class_name("button-container-search").click()
            time.sleep(1)
            #pageDriver.find_element_by_class_name("button-container-search").click()
            #Ждем пару секунд для прогрузки, на сайте vue, бывает тупит
            #time.sleep(1)

            #Проверяем, есть ли блок с информацией, если нет, значит ничего не найдено
            regionInfoBlock = pageDriver.find_elements_by_class_name('detail-info')

            if not len(regionInfoBlock) == 0:
                while True:
                    status = self.resizeMap(pageDriver)
                    if(status == 1):
                        break

                return regionInfoBlock, pageDriver

            else:
                #Возвращаем код 1 - ничего не найдено
                return 1
        else:
            #Возвращаем код 0 - сайт недоступен
            return 0

    def resizeMap(self, webDriver):
        buttonToResize = webDriver.find_element_by_css_selector("div[title='Приблизить']")
        scaleFactor = webDriver.find_element_by_class_name('esri-scale-bar__label').text

        if int(re.findall(r'\d+', scaleFactor)[0]) > 15:
            buttonToResize.click()
            self.resizeMap(webDriver)
            return 0
        else:
            return 1


