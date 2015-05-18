import json
import csv

with open('d3-0515_7pt6_intlist.json','r') as file:
    data = json.load(file)
    file.close()
print data['topteninterests']

dict = {}
for item in data['topteninterests']:
    dict[item.keys()[0]] = item.values()[0]
print dict

f = csv.writer(open('d3-0515_7pt6_intlist.csv','w'))
f.writerow(["name", "freq"])
for key, value in dict.items():
   f.writerow([key, value])

