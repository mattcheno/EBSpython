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
import csv, ctypes, sys, os, re #, math, random #commented modules not needed
#ebsFile = open('ebsCSVData.csv')     # Input file
ebsFile = open('sample.csv')
ebsReader = csv.reader(ebsFile)
exFile = open('exceptions.csv', 'w', newline='')     # exceptions file
exWriter = csv.writer(exFile)
outputFile = open('output.csv', 'w', newline='')     # output file
outputWriter = csv.writer(outputFile)
manfKeyFile = open('Key_ManfCodes.csv')     # Key File to fix Manufacturers
manfKeyReader = csv.reader(manfKeyFile)
manKeyDict = {}
mamoKeyFile = open('Key_MakeModels.csv')     #Key File for Makes and Models
mamoKeyReader = csv.reader(mamoKeyFile)
mamoKeyDict = {}
def mBox(title, text, style): # Message Box Function
    ctypes.windll.user32.MessageBoxW(0, text, title, style)
j = 0
k = 0
nullRgX = re.compile(r'unk.*|(x){2,}|N/A', re.I) #Null-Value RegEx


# --- Logic -------------------------------------------------------------------

# Create Manufacturers Key Dictionary
for row in manfKeyReader:
	if mamoKeyReader.line_num == 1:
		continue
	else:
		manKeyDict[row[0]] = row[1]
	
manfKeyFile.close()

# Create UnitType Key Dictionary

mamoKeyFile.close()

# Iterate through each line in the original CSV
for row in ebsReader:
	k = ebsReader.line_num

	# Add Key Field
	if ebsReader.line_num == 1:
		row.insert(0, 'Key')
		outputWriter.writerow(row)
		row.append('NOTES')
		exWriter.writerow(row)
		continue
	else:
		row.insert(0, ebsReader.line_num - 1)

	# Strip Time stamp from OrderDate field (row[14])
	try:
		row[14]=row[14].split()[0]
	except IndexError:
		continue
	
	# Dictionary look up for Manf Code (row[5])
	newManf = manKeyDict.get(row[5], 'NA')
	
	# NA replacement
	for i in range(len(row)):
		if row[i] == '': row[i] = 'NA'
		row[i] = nullRgX.sub('NA', str(row[i]))

	# Writes row to output if model code isn't null
	if row[6] == 'NA':     # ModelCode (row[6]) for NA values
		row.append('ModelCode contains NA value')
		exWriter.writerow(row)
		continue
	elif newManf == 'NA':     # Manf Code isn't in Key File
		row.append('Manufacturer not found in Key File')
		exWriter.writerow(row)
		continue
	else:
		row[5] = newManf
		outputWriter.writerow(row)
		j = j + 1
	
#end of for loop

mess='Complete: '+str(100*j/k)+'%\nJ= '+str(j)+'\nK= '+str(k)+' /3,003,715'
# --- Close Files -------------------------------------------------------------
ebsFile.close()
outputFile.close()
exFile.close()
mBox('DONE',mess, 1)

# === FOOTNOTES ===============================================================
# === END OF CODE =============================================================
