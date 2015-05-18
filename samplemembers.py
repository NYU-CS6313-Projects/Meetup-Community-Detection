import pandas
import random

members_data=[]
with open('samplemembernames.txt', 'r') as infile:
        temp = infile.readlines()
        members_filenames = []
        for ele in temp:
            members_filenames.append(ele.strip('\n'))
        #print members_filenames[0]

for file in range(len(members_filenames)):
    json_data = open(members_filenames[file])
    members_data.append(pandas.io.json.read_json(json_data))

#members_df=pandas.concat(members_data)
#members_df.to_csv('memberssample.csv',encoding='utf-8')

id = random.sample(xrange(len(members_filenames)), int(0.01*len(members_filenames)))
print id

for e in id:


"""
# write to csv
l = []
for i in id:
    l.append(members_filenames[i])
"""
