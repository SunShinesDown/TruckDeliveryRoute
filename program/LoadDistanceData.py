import csv
from re import L


def loadDistanceData(distanceData):
    data = open("CSVFiles\\distanceData.csv")
    csvData = csv.reader(data)
    listOfRows = list(csvData)
    for row in listOfRows[8:]:
        distanceData.append(row[2:])
    data.close()


def loadAddressData(addressData):
    data = open("CSVFiles\\distanceData.csv")
    csvData = csv.reader(data)
    listOfRows = list(csvData)
    addressData.append("HUB")
    for address in listOfRows[9:]:
        stAddress = address[1].split("(")[0].strip()
        stAddress = stAddress.replace(" S ", " South ")
        stAddress = stAddress.replace(" W ", "West")
        stAddress = stAddress.replace(" E ", " East ")
        stAddress = stAddress.replace(" N ", " North ")
        addressData.append(stAddress)
    data.close()
