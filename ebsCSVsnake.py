#! python3

#==============================================================BOILERPLATE=====
#
#  EBS CSV pre-conditioner
#  Matthew Chenoweth
#  2016/10/27
#
#  Using the Power of Python to iteratively check the Massive CSV file from EBS
# to ease the entry into R.
#  The Scope is ONLY for the "first pass"
#  Note: There are 3,003,714 observations in the first pass


#-------------------------------------------------------------Declarations-----
import time   #Time Functions for run-time tracking
tStart = time.time()
import csv  #Read/Write CSV Files
import ctypes   #Message Box Functionality
import sys   #
import os   #Functions for working with different OSes
import re   #RegEx!! 
ebsFile = open('ebsCSVData.csv')     # Input file
#ebsFile = open('sample.csv')         # Sample file
ebsReader = csv.reader(ebsFile)
exFile = open('exceptions.csv', 'w', newline='')     # exceptions file
exWriter = csv.writer(exFile)
outputFile = open('output.csv', 'w', newline='')     # output file
outputWriter = csv.writer(outputFile)
unitKeyDict = {}  #Dictionary for Unit Type Lookup
manfKeyDict = {}  #Dictionary for Manufacturer Lookup
moYrKeyDict = {}  #Dictionary for ModelYear
def mBox(title, text, style): # Message Box Function
    ctypes.windll.user32.MessageBoxW(0, text, title, style)
j = 0  #counter, successful writes
k = 0  #counter, total iterations
m = 0  #counter, percentage status
e1 = 0  #counter, 'ModelCode contains NA value'
e2 = 0  #counter, 'Manufacturer not found in Key File'
e3 = 0  #counter, 'Model not found in Key File'
e4 = 0  #counter, 'Meter is not numeric'
e5 = 0  #counter, 'Model Year not found in Key File'
z = 0  #counter, number of zero Meter readings
nullRgX = re.compile(r'unk.*|(x){2,}|N/A', re.I) #Null-Value RegEx
dashRgX = re.compile(r'-|/') #Dashes or Slashes RegEx
def errRep(eN, eMess, tot):
	erString = (str(eN) + ' (' + str(round(100 * eN / max(tot, 1), 4)) + 
	'%) :: ' + eMess + '\n')
	return erString

#mBox('Go', 'Go', 1)
#--------------------------------------------------------------------Logic-----

# Create Unit Type Dictionary
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

# Iterate through each line in the original CSV
for row in ebsReader:
	k = ebsReader.line_num

	# Print percentage Status Update
	if k % 300371 == 0:    # 1% should be 30,030
		tDur = round(time.time() - tStart)
		m = m + 1
		print(str(k) + ' rows (' + str(m) + '0%) in ' + str(tDur) + ' seconds')
	
	# Add Key Field
	if ebsReader.line_num == 1:
		row.insert(0, 'Key')
		outputWriter.writerow(row)
		row.append('NOTES')
		exWriter.writerow(row)
		continue
	else:
		row.insert(0, ebsReader.line_num - 1)

	# NA replacement
	for i in range(len(row)):
		if row[i] == '': row[i] = 'NA'
		row[i] = nullRgX.sub('NA', str(row[i]))

	# Strip Time stamp from OrderDate field (row[14])
	try:
		row[14]=row[14].split()[0]
	except IndexError:
		continue
	
	# Strip Dashes from ModelCode (row[6])
	row[6] = dashRgX.sub('', row[6])
	
	# Dictionary look up for Manf Code (row[5])
	newManf = manfKeyDict.get(row[5], 'NA')
	
	# Dictionary look up for UnitType
	makeDict = unitKeyDict.get(row[5], 'ERR01')  #-----------Footnote 001
	if type(makeDict) is dict:
		uType = makeDict.get(row[6], 'NA') #row[6] is 'Model'
	
	# Dictionary look up for Model Year
	yearDict = moYrKeyDict.get(row[5], 'ERR02')
	if type(yearDict) is dict:
		moYear = yearDict.get(row[6], 'NA') #row[6] is 'Model'
	
	# Writes row to output if model code isn't null
	if row[6] == 'NA':     # ModelCode (row[6]) for NA values
		row.append('ModelCode contains NA value')
		e1 = e1 + 1
		exWriter.writerow(row)
		continue
	elif newManf == 'NA':     # Manf Code isn't in Key File
		row.append('Manufacturer not found in Key File')
		e2 = e2 + 1
		exWriter.writerow(row)
		continue
	elif uType == "NA":
		row.append('Model not found in Key File')
		e3 = e3 + 1
		exWriter.writerow(row)
		continue
	elif moYear == "NA":
		row.append('Model Year not found in Key File')
		e5 = e5 + 1
		exWriter.writerow(row)
		continue
	else:
		try:  #----------------------------------------------Footnote 002
			if int(row[9]) < 1: z = z + 1    # row[9] is Meter reading
		except ValueError:
			row.append('Meter is not numeric')
			e4 = e4 + 1
			exWriter.writerow(row)
			continue
		row[5] = newManf
		row[15] = moYear     # row[15] is 'EquipYear'
		row[16] = uType     # row[16] is 'Class'
		outputWriter.writerow(row)
		j = j + 1
	
#end of for loop

	
#--------------------------------------------------------------Close Files-----
ebsFile.close()
outputFile.close()
exFile.close()
runStats = ('Complete: ' + str(round(100 * j / k, 4)) +
	'%\nJ= ' + str(j) +
	'\nK= ' + str(k) + ' /3,003,715\n' +
	errRep(e1, 'ModelCode contains NA value', k) +
	errRep(e2, 'Manufacturer not found in Key File', k) +
	errRep(e3, 'Model not found in Key File', k) +
	errRep(e4, 'Meter not numeric', k) +
	errRep(e5, 'Model Year not found in Key File', k) + 
	'----------\n' +
	errRep(z, 'Meter Value Zero, Percent of Complete', j) + 
	'==========\n' +
	str(round(time.time() - tStart, 2)) + ' Total Seconds Runtime')
#mBox('DONE',runStats, 1)
repFile = open('csvReport.txt', 'w')
repFile.write(runStats)
repFile.close()
print(runStats)

#================================================================FOOTNOTES=====
#    Note 001
# Look up the three-digit MFG code (row[5]) from the observation in the UberKey
# dictionary and assign the nested dictionary of models/unit-types to makeDict
# variable. Assign "ERR01" code if MFG code not found.
#    Note 002
# Test for non-numeric Meter field value in other-wise successful observations
#==============================================================END OF CODE=====
