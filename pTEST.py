#! python3

import csv
import pprint

unitKeyDict = {}  #Dictionary for Unit Type Lookup
manfKeyDict = {}  #Dictionary for Manufacturer Lookup
moYrKeyDict = {}  #Dictionary for ModelYear

with open("UberKey.csv", 'r') as data_file:     #UberKey File
	data = csv.DictReader(data_file, delimiter = ",")
	for row in data:
		#Manufacturer Dictionary
		manfKeyDict[row["Mfg"]] = row["Manufacturer"]
		#UnitType Dictionary
		item = unitKeyDict.get(row["Mfg"], dict())
		item[row["Model"]] = row["UnitType"]
		unitKeyDict[row["Mfg"]] = item
		#ModelYear Dictionary
		myItem = moYrKeyDict.get(row["Mfg"], dict())
		myItem[row["Model"]] = row["Year"]
		moYrKeyDict[row["Mfg"]] = myItem

repFile = open('pprint.txt', 'w')
#repFile.write(pprint.pformat(unitKeyDict))
repFile.write(pprint.pformat(moYrKeyDict))
repFile.close()
