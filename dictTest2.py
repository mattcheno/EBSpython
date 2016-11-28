import csv, ctypes, sys, os, re

mamoKeyFile = open('Key_MakeModels.csv')     # Key File for Makes and Models
mamoKeyReader = csv.reader(mamoKeyFile)
mamoKeyDict = {}

for row in mamoKeyReader:
    if mamoKeyReader.line_num == 1:
        continue
    else:
        #<----------

for k, v in manKeyDict.items():
    print('Key: ' + k + ' Value: ' + v)
