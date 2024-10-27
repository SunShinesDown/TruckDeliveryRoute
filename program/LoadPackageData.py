import csv
from os import close
from Package import Package


def loadPackageData(hashMap):
    data = open("CSVFiles\\packageData.csv", encoding="utf-8")
    csvData = csv.reader(data)
    dataInRows = list(csvData)
    for row in dataInRows[8:]:
        key = int(row[0])
        address = row[1].replace(" S ", " South ")
        address = address.replace(" W ", "West")
        address = address.replace(" E ", " East ")
        address = address.replace(" N ", " North ")
        package = Package(row[0], address, row[5], row[2], row[4], row[6], row[7])
        hashMap.insert(key, package)
    data.close()
