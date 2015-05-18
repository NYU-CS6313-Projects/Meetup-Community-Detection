import json
import random
import math
import operator
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from itertools import product

l = []
idlist = [] # this stores id and corresponding interests
idname = []
with open('merged_file0.json','r') as file:
    data = json.load(file)
    for i in data:
        #print type(i),i["id"]
        topics = []
        dict = {}
        idnamedic = {}
        idnamedic[i['id']] = i['name']
        idname.append(idnamedic)
        dict['id'] = i["id"]
        #dict['group'] = 1
        for e in i['topics']:
            topics.append(e["name"])
        #print topics
        idd = {}
        idd[i['id']] = topics
        if idd[i['id']] != []:
            idlist.append(idd)
        l.append(dict)
# print idlist[:8]
#print len(idlist)
# print "name is",len(idname),idname

alltopics = []
for item in idlist:
    alltopics.extend(item.values()[0])
# print alltopics[:10]

# print "total int",len(alltopics)
print Counter(alltopics)
print len(Counter(alltopics))
toptenint = Counter(alltopics).most_common(150)
print "look here",toptenint[-1]
top = []
for i in toptenint:
    top.append(i[0])
print top

intlist_sort = sorted(Counter(alltopics).items(),key=lambda x: x[1],reverse=True)
# print intlist_sort
# get least popular topic
# print intlist_sort[-1]
# print len(intlist_sort)
# print toptenint

# occur = []
# topic = []
# for e in intlist_sort:
#     topic.append(e[0])
#     occur.append(e[1])

#print "need",np.median(np.asarray(occur))
# Find how many members have topteninterests in their topics
# mem = []
# for e in idlist:
#     s = e.values()[0]
#     for t in topic:
#         if t in s:
#             if e.keys()[0] not in mem:
#                 mem.append(e)
# print len(mem)
# print mem[:10]

# Carefully select interests to plot,ideally, creat 4 clusters with most common interest and inerests around 30, then assign
# group based on common interests, prepare in form of idlist, use Machine Learning and Data Visualization, and top2:
# Live Music and Anime. first check overlap of top2 and Machine Learning and Data Visualization

# check overlap of top2
# overlap2 = []
# for sth in mem:
#     if 'Live Music' in sth.values()[0] and 'Anime' in sth.values()[0]:
#         overlap2.append(sth)
# print "overlap top 2 interest", len(overlap2)

# Since top2 have so many overlap members, choose 'Dating and Relationships' to represent middle range interests
# now the cluster should be ["Machine Learning","Data Visualization","Dating and Relationships","Live Music"]
# prepare these idlist
intid1 = []
intid2 = []
intid3 = []
intid4 = []
for i in idlist:

    #print i
    # print "compare",len(i.values()[0])
    # remove top ten interest first
    l3 = [x for x in i.values()[0] if x not in top]
    i[i.keys()[0]] = l3
    # print "l3",len(l3)
    if "Machine Learning" in l3 and 'Science Fiction & Fantasy Books' not in l3 \
            and 'Literature' not in l3:
        intid1.append(i)
    elif 'Science Fiction & Fantasy Books' in l3 and 'Data Analytics' not in l3 \
            and "Machine Learning" not in l3:
        intid2.append(i)
    elif 'Literature' in l3 and "Machine Learning" not in l3 and 'Data Analytics' not in l3:
        intid3.append(i)
    elif 'Data Analytics' in l3 and 'Science Fiction & Fantasy Books' not in l3 and 'Literature' not in l3 \
    :
        intid4.append(i)
print len(intid1),len(intid2),len(intid3),len(intid4)
# print intid1
print intid3
# plt.hist(occur)
# plt.show()

# # Want to count word co-occurrences of Machine Learning
# # Create ML big list
# ML = []
# for i in intid1:
#     ML.extend(i.values()[0])
# print ML
# # Count ML co-occurences with other topics
# # c = Counter((x, y) for x,y in enumerate(ML))
# # for i in product(ML):
# #     print i
# # print "look",c
# r = []
# for x,y in ML:
#     if x == "Machine Learning":
#         r.append(Counter(x,y))
# print "lokk",r
