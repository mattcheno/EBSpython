import csv

new_data_dict = {}
with open("Key_MakeModels.csv", 'r') as data_file:
    data = csv.DictReader(data_file, delimiter=",")
    for row in data:
        item = new_data_dict.get(row["Make"], dict())
        item[row["Model"]] = row["UnitType"]

        new_data_dict[row["Make"]] = item

print(new_data_dict)