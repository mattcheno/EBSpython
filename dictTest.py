import csv, ctypes, sys, os, re

manfKeyFile = open('Key_ManfCodes.csv')     # Key File to fix Manufacturers
manfKeyReader = csv.reader(manfKeyFile)
manKeyDict = {}

for row in manfKeyReader:
    manKeyDict[row[0]] = row[1]

for k, v in manKeyDict.items():
    print('Key: ' + k + ' Value: ' + v)
