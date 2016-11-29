import csv

manKeyDict = {}

with open("Key_ManfCodes.csv", 'r') as data_file:
    data = csv.DictReader(data_file, delimiter = ",")
    for row in data:
        manKeyDict[row["Code"]] = row["Name"]

#import csv, ctypes, sys, os, re

#manfKeyFile = open('Key_ManfCodes.csv')     # Key File to fix Manufacturers
#manfKeyReader = csv.reader(manfKeyFile)
#manKeyDict = {}

#for row in manfKeyReader:
#    manKeyDict[row[0]] = row[1]

for k, v in manKeyDict.items():
    print('Key: ' + k + ' Value: ' + v)
