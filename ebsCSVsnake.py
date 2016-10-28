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
import csv
import ctypes
ebsFile = open('ebsCSVData.csv')
ebsReader = csv.reader(ebsFile)
archiveFile = open('archive.csv', 'w', newline='')
archiveWriter = csv.writer(archiveFile)
outputFile = open('output.csv', 'w', newline='')
outputWriter = csv.writer(outputFile)
def mBox(title, text, style):
    ctypes.windll.user32.MessageBoxW(0, text, title, style)
j = 0
k = 0


# --- Logic -------------------------------------------------------------------

# Iterate through each line in the original CSV
for row in ebsReader:
	k = ebsReader.line_num

	# Add Key Field
	if ebsReader.line_num == 1:
		row.insert(0, 'Key')
	else:
		row.insert(0, ebsReader.line_num - 1)

	# Strip Time stamp from OrderDate field (row[14])
	try:
		row[14]=row[14].split()[0]
	except IndexError:
		continue

	# NA replacement
	for i in range(len(row)):
		if row[i] == '':
			row[i] = 'NA'
		elif row[i] == 'N/A':
			row[i] = 'NA'
		elif row[i] == 'UNK':
			row[i] = 'NA'
		elif row[i] == 'UNKNOWN':
			row[i] = 'NA'
		elif row[i] == 'XXX':
			row[i] = 'NA'
		elif row[i] == 'XXXX':
			row[i] = 'NA'
		elif row[i] == 'XXXXX':
			row[i] = 'NA'
		elif row[i] == 'XXXXXXXXX':
			row[i] = 'NA'
		elif row[i] == 'XXXXXXXXXXX':
			row[i] = 'NA'

	# Writes row to output if model code isn't null
	if row[6] == 'NA':     # ModelCode (row[6]) for NA values
		continue
	elif row[5].upper() == 'CAS':     # Mfg (row[5]) for Cascade
		continue
	else:
		outputWriter.writerow(row)
		j = j + 1
#end of first for loop

mess='Complete: '+str(100*j/k)+'%\nJ= '+str(j)+'\nK= '+str(k)+' /3,003,715'
# --- Close Files -------------------------------------------------------------
ebsFile.close()
outputFile.close()
archiveFile.close()
mBox('DONE',mess, 1)

# === FOOTNOTES ===============================================================
# === END OF CODE =============================================================
