import argparse
import readExcel
import regisrtyRequest
import region
import registryMap
import filter
import pandas as pd
import openpyxl
from rosreestr2coord import Area


def processRegistryNumbers(numbersList, columnName):
    reportArray = [['Тип',
                    'Вид',
                    'Кадастровый номер',
                    'Кадастровый квартал',
                    'Статус',
                    'Адрес',
                    'Категория земель',
                    'Форма собственности',
                    'Кадастровая стоимость',
                    'Дата определения КС',
                    'Дата внесения сведений о КС',
                    'Дата утверждения КС',
                    'Дата применения КС',
                    'Уточненная площадь',
                    'Разрешенное использование',
                    'По документу',
                    #'Размер желтой площади'
                    #'Размер красной площади',
                    'Размер зеленой площади',
                    #'Соотношение',
                    'Есть ли особая зона на участке'
                    ]]
    for index,x in enumerate(numbersList[columnName]):
        regisrtyObject = regisrtyRequest.registryRequest(x)
        try:
            regionInfoBlock, pageDriver = regisrtyObject.loadPage()
        except TypeError:
            reportArray.append([
                '',
                '',
                x,
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                # 'Размер желтой площади'
                # 'Размер красной площади',
                '',
                # 'Соотношение',
                'По данному кадастровому номеру ничего не найдено'

            ])

            continue

        if(regionInfoBlock == 0):
            print("Сайт росеестра недоступен, попробуйте попозже")
            break
        elif (regionInfoBlock == 1):
            print("По данному кадастровому номеру ничего не найдено")
            continue
        else:
            regionInfo = region.Region(regionInfoBlock)
            # Для Вани, можешь закомметировать все, что ниже, если тебе нужны только данные.
            #TODO метод вернул нам массив с данными по участку, записываем его куда нибудь.
            # после завершения обязательно сохранить в корень
            tempRegionInfoArray = regionInfo.extractInfo()
            registryMapObject = registryMap.Map(pageDriver, x)

            croppedImage, registryMapSavePath = registryMapObject.getScreenShot(x)

            # filteredAreaGreen = filter.Filter(croppedImage, 26, 160, 220, 255, 255, 255, 'green', registryMapSavePath)

            # try:
            #     filteredAreaGreenContour, filteredGreenAreaValue = filteredAreaGreen.getContour()
            #     tempRegionInfoArray.append(filteredGreenAreaValue)
            #     if filteredGreenAreaValue > 20:
            #         tempRegionInfoArray.append("Найдена зона с особым использованием")
            #     else:
            #         tempRegionInfoArray.append("Не найдено")
            filteredAreaYellow = filter.Filter(croppedImage, 12,111,250,121,248,255, 'yellow', registryMapSavePath)
            try:
                filteredAreaYellowContour, filteredYellowAreaValue = filteredAreaYellow.getContour()
                filteredAreaRed = filter.Filter(filteredAreaYellowContour, 0, 44, 55, 25, 255, 255, 'red',
                                               registryMapSavePath)
                filteredAreaRedContour, filteredRedAreaValue = filteredAreaRed.getContour()

                # filteredAreaGreen = filter.Filter(filteredAreaYellowContour, 5, 102, 0, 255, 255, 255, 'green',
                #                                registryMapSavePath)
                # filteredAreaRedContour, filteredRedAreaValue = filteredAreaGreen.getContour()

                #Добавляем значения во временный массив
                tempRegionInfoArray.append(filteredYellowAreaValue)
                tempRegionInfoArray.append(filteredRedAreaValue)
                #Добавляем решение есть ли дом на участке
                if ((filteredRedAreaValue / filteredYellowAreaValue) * 100 > 0.5):
                    tempRegionInfoArray.append(1)
                else:
                    tempRegionInfoArray.append(0)
            except IndexError:
                tempRegionInfoArray.append(0)
                tempRegionInfoArray.append("Не найдено")


            reportArray.append(tempRegionInfoArray)
            #Удаляем временный массив
            del tempRegionInfoArray

        if index % 100 == 0:
            outputDF = pd.DataFrame(reportArray)
            outputDF.to_excel('report-green.xlsx')




if __name__ == "__main__":
    # Считываем нужный файл из консоли
    parser = argparse.ArgumentParser()

    #parser.add_argument("-f", dest='fileLink', help="link to excel file")
    #parser.add_argument('-column', dest='columnToProcess', help='column in dataframe, that contains registry numbers', type=str)
    #args = parser.parse_args()

    excelFile = readExcel.ExcelDocument('process.xlsx')
    processRegistryNumbers(excelFile.readExcel(), 'number')