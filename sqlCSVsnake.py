#! python3

# === BOILERPLATE =============================================================
#
#  EBS CSV pre-conditioner
#  Matthew Chenoweth
#  2016/12/08
#
#   Taking output from Patrick's SQL Join of EBS data and converting it to 
#  format for BOC


# --- Declarations ------------------------------------------------------------
import time # time module for tracking script runtime
tStart = time.time()
import csv # CSV module for reading/writing csv files
import re # RegEx module for null-value substitution
inputFile = open('sqlCSVData.csv')  # input file
csvReader = csv.reader(inputFile)
exFile = open('exceptionsSQL.csv', 'w', newline='')     # exceptions file
exWriter = csv.writer(exFile)
outputFile = open('outputSQL.csv', 'w', newline='')     # output file
outputWriter = csv.writer(outputFile)
nullRgX = re.compile(r'unk.*|(x){2,}|N/A', re.I) #Null-Value RegEx
j = 0  # successfull write counter
k = 0  # iteration counter
#header = ['WieseID','WorkOrder','OrderDate','Manufacturer','Model','UnitType','Class','Subclass','EquipYear','Branch','Segment','OrderType','SerialNumber','Meter','Labor','Parts','Misc','Total']


# --- Logic -------------------------------------------------------------------

for row in csvReader:
    k = csvReader.line_num

    #Status Update
    if k % 10000 == 0:
        tDur = round(time.time() - tStart)
        print(str(k) + ' rows in ' + str(tDur) + ' seconds')

    #<<<----
#for-loop END
