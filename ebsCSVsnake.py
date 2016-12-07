#! python3

# === BOILERPLATE =============================================================
#
#  EBS CSV pre-conditioner
#  Matthew Chenoweth
#  2016/10/27
#
#  Using the Power of Python to iteratively check the Massive CSV file from EBS
# to ease the entry into R.
#  The Scope is ONLY for the "first pass"
#  Note: There are 3,003,714 observations in the first pass


# --- Outline -----------------------------------------------------------------
# 1. Declarations
# 2. Logic
# 3. Close Files

# --- Declarations ------------------------------------------------------------
import time
tStart = time.time()
import csv, ctypes, sys, os, re #, math, random #commented modules not needed
ebsFile = open('ebsCSVData.csv')     # Input file
#ebsFile = open('sample.csv')         # Sample file
ebsReader = csv.reader(ebsFile)
exFile = open('exceptions.csv', 'w', newline='')     # exceptions file
exWriter = csv.writer(exFile)
outputFile = open('output.csv', 'w', newline='')     # output file
outputWriter = csv.writer(outputFile)
manKeyDict = {}
mamoKeyDict = {}
def mBox(title, text, style): # Message Box Function
    ctypes.windll.user32.MessageBoxW(0, text, title, style)
j = 0
k = 0
m = 0
x = 0
y = 0
z = 0
nullRgX = re.compile(r'unk.*|(x){2,}|N/A', re.I) #Null-Value RegEx


# --- Logic -------------------------------------------------------------------

# Create Manufacturers Key Dictionary
with open("Key_ManfCodes.csv", 'r') as data_file:
    data = csv.DictReader(data_file, delimiter = ",")
    for row in data:
        manKeyDict[row["Code"]] = row["Name"]

# Create UnitType Key Dictionary
with open("Key_MakeModels.csv", 'r') as data_file:     #Make/Model Key File
	data = csv.DictReader(data_file, delimiter = ",")
	for row in data:
		item = mamoKeyDict.get(row["Make"], dict())
		item[row["Model"]] = row["UnitType"]
		mamoKeyDict[row["Make"]] = item

		
# Iterate through each line in the original CSV
for row in ebsReader:
	k = ebsReader.line_num

	# Percentage Status Update
	if k % 300371 == 0:    # 1% should be 30,030
		tDur = round(time.time() - tStart)
		m = m + 1
		print(str(k) + ' rows in ' + str(tDur) + ' seconds (' + str(m) + '0%)')
	
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
	
	# Dictionary look up for Manf Code (row[5])
	newManf = manKeyDict.get(row[5], 'NA')
	
	# Dictionary look up for UnitType
	makeDict = mamoKeyDict.get(newManf, 'ERR01')
	if type(makeDict) is dict:
		uType = makeDict.get(row[6], 'NA') #row[6] is 'Model'
	
	# Writes row to output if model code isn't null
	if row[6] == 'NA':     # ModelCode (row[6]) for NA values
		row.append('ModelCode contains NA value')
		exWriter.writerow(row)
		continue
	elif newManf == 'NA':     # Manf Code isn't in Key File
		row.append('Manufacturer not found in ManfCode Key File')
		x = x + 1
		exWriter.writerow(row)
		continue
	elif type(makeDict) is str:
		row.append('Manufacturer not found in Make/Model Key File')
		y = y + 1
		exWriter.writerow(row)
		continue
	elif uType == "NA":
		row.append('Model not found in Make/Model Key File')
		z = z + 1
		exWriter.writerow(row)
		continue
	else:
		row[5] = newManf
		row[16] = uType     # row[16] is 'Class'
		outputWriter.writerow(row)
		j = j + 1
	
#end of for loop

runStats = ('Complete: ' + str(100*j/k) +
	'%\nJ= ' + str(j) +
	'\nK= ' + str(k) + ' /3,003,715\n' +
	str(x) + ' (' + str(round(x/k)) +
	'%) :: Manufacturer not found in ManfCode Key File\n' +
	str(y) + ' (' + str(round(y/k)) +
	'%) :: Manufacturer not found in Make/Model Key File\n' +
	str(z) + ' (' + str(round(z/k)) +
	'%) :: Model not found in Make/Model Key File\n' +
	str(round(time.time() - tStart, 4 )) + ' Total Seconds Runtime')
	
# --- Close Files -------------------------------------------------------------
ebsFile.close()
outputFile.close()
exFile.close()
#mBox('DONE',runStats, 1)
print(runStats)

# === FOOTNOTES ===============================================================
# === END OF CODE =============================================================
