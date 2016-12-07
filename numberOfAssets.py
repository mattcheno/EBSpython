nAss = {}
import csv, pprint

csvFile = open('ebsCSVData.csv')
csvReader = csv.reader(csvFile)
outFile = open('NumberOfAssets.txt', 'w')

for row in csvReader:
    if csvReader.line_num == 1:
        outFile.write(str(row[7]) + '\n')
        continue
    else:
        try:
            wID = str(row[7])
            nAss.setdefault(wID, 0)
            nAss[wID] = nAss[wID] + 1
        except IndexError:
            continue


outFile.write(pprint.pformat(nAss))#<-----
outFile.write(str(len(nAss)))

csvFile.close()
outFile.close()
