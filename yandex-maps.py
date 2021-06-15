import argparse
import readExcel
import regisrtyRequest
import region
import registryMap
import filter
import pandas as pd
import openpyxl
from rosreestr2coord import Area
import os
import urllib
import requests

import shutil


def processRegistryNumbers(numbersList, columnName):
    counter = 0
    for x in numbersList[columnName]:
        counter += 1
        print(counter)
        registryNumber = x.replace(':','')
        #output_path = './yandex-maps/' + registryNumber
        # Создаем папку под кадастровый номер
        # Получение координат каждого участка, занесение в лист

        coord_list = []
        area = Area(x)

        coord_list.insert(0, area.get_coord())
        try:
            coord_list[0].append(coord_list[0][0][0][0])

            coord = '~'.join(str(v) for v in coord_list)
            str1 = ''.join(n for n in coord if n.isdigit() or n == '.' or n == ',' or n == '~')

            url = "https://static-maps.yandex.ru/1.x/?l=sat&pl=" + str1
            response = requests.get(url, stream=True)
            with open('./yandex-maps-output/' + registryNumber + '.jpg', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response

            #urllib.request.urlretrieve("https://static-maps.yandex.ru/1.x/?l=sat&pl=" + str1, './yandex-maps-output/' + registryNumber + '.jpg')


        except IndexError:
            print('Нет координат, пропускаем')
            pass
        # Обработка




if __name__ == "__main__":
    # Считываем нужный файл из консоли
    parser = argparse.ArgumentParser()

    #parser.add_argument("-f", dest='fileLink', help="link to excel file")
    #parser.add_argument('-column', dest='columnToProcess', help='column in dataframe, that contains registry numbers', type=str)
    #args = parser.parse_args()

    excelFile = readExcel.ExcelDocument('process.xlsx')
    processRegistryNumbers(excelFile.readExcel(), 'number')