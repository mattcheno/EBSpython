nAss = {}
import csv, pprint

csvFile = open('ebsCSVData.csv')
csvReader = csv.reader(csvFile)
outFile = open('results.txt', 'w')

for row in csvReader:
    if csvReader.line_num == 1:
        print(str(row[7]))
        continue
    else:
        try:
            wID = str(row[7])
            nAss.setdefault(wID, 0)
            nAss[wID] = nAss[wID] + 1
        except IndexError:
            continue


print(pprint.pformat(nAss))#<-----
print(str(len(nAss)))

csvFile.close()
outFile.close()
