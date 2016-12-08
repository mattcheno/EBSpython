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
inputFile = open('sqlCSVData.csv')  # input file (ASSUMING UTF-8!!!!!!)
csvReader = csv.reader(inputFile)
exFile = open('exceptionsSQL.csv', 'w', newline='')     # exceptions file
exWriter = csv.writer(exFile)
outputFile = open('outputSQL.csv', 'w', newline='')     # output file
outWriter = csv.writer(outputFile)
nullRgX = re.compile(r'unk.*|(x){2,}|N/A', re.I) #Null-Value RegEx
dshRgX = re.compile(r'')  #dash and slash RegEx
z = 0  # iteration counter
y = 0  # successfull write counter
x = 0  # NA Model counter


# --- Logic -------------------------------------------------------------------

for row in csvReader:
    z = csvReader.line_num

    #Status Update
#    if z % 10000 == 0:
#        tDur = round(time.time() - tStart)
#        print(str(z) + ' rows in ' + str(tDur) + ' seconds')

    #Add Index Field
    if csvReader.line_num == 1:
        row.insert(0,'Index')
        outWriter.writerow(row)
        row.append('NOTES')
        exWriter.writerow(row)
        continue
    else:
        row.insert(0, csvReader.line_num - 1)

    #NA replacement
    for i in range(len(row)):
        if row[i] == '': row[i] = 'NA'
        row[i] = nullRgX.sub('NA', str(row[i]))

    #Writing
    if row[5] == 'NA': # row[5] is "Model"
        x = x + 1
        row.append('Model contains NA value')
        exWriter.writerow(row)
        continue
    else:
        y = y + 1
        outWriter.writerow(row)
    #<<<----
#for-loop END

#Report Run-time Statistics, clean up
inputFile.close()
exFile.close()
outputFile.close()
runStats = ('Completion %: ' + str(round(100 * y / 3003714, 2)) +
    '\nC% of second pass: ' + str(round(100 * y / z, 2)) +
    '\nNumber successfully writen :' + str(y) +
    '\nModel contains NA value: ' + str(x) +
    '\nTotal Seconds Runtime: ' + str(round(time.time() - tStart, 4 )))
repFile = open('sqlReport.txt', 'w')
repFile.write(runStats)
repFile.close()
print(runStats)
# === FOOTNOTES ===============================================================
# === END OF CODE =============================================================
