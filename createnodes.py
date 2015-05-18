import json
import random
import math
import operator

l = []
l1 = []
idlist = []
idname = []
idlist1 = []
idname1 = []
statelist = []
statelist1 = []

with open('merged_file0.json','r') as file:
    data = json.load(file)
    for i in data:
        if "state" in i:
            if i["state"] == "CA":
                topics = []
                dict = {}
                idnamedic = {}
                statedic = {}
                statedic[i['id']] = i['state']
                idnamedic[i['id']] = i['name']
                idname.append(idnamedic)
                statelist.append(statedic)
                dict['id'] = i["id"]
                dict['group'] = i["state"]
                for e in i['topics']:
                    topics.append(e["id"])
                idd = {}

                idd[i['id']] = topics
                if idd[i['id']] != []:
                    idlist.append(idd)
            if i["state"] == "NY":
                topics1 = []
                dict1 = {}
                idnamedic1 = {}
                statedic1 = {}
                statedic1[i['id']] = i['state']
                idnamedic1[i['id']] = i['name']
                idname1.append(idnamedic1)
                statelist1.append(statedic1)
                dict1['id'] = i["id"]
                dict1['group'] = i["state"]
                for e1 in i['topics']:
                    topics1.append(e1["id"])
                idd1 = {}
                #print "topics is", topics
                idd1[i['id']] = topics1
                if idd1[i['id']] != []:
                    idlist1.append(idd1)
        l.append(dict)
        l1.append(dict1)

idnameall = idname+idname1

# random sample same number of data points from NY and CA
CAlist = random.sample(idlist,25)
NYlist = random.sample(idlist1,25)

idlist = NYlist+CAlist

pairlist = []
for k in range(len(idlist)):
    #print "k is",k
    l_without_k = idlist[(k + 1):]
    kval = idlist[k].values()[0]
    #print "look",kval
    if kval!= []:
        # print "kval is",kval
        for ele_dic in l_without_k:
            #print "ele_dic is", ele_dic
            dic_temp = {}
            dic_temp[(idlist[k].keys()[0],ele_dic.keys()[0])] = []
            for a in kval:
                #print "a is",a
                if a in ele_dic.values()[0]:
                    #print "you"
                    dic_temp[(idlist[k].keys()[0],ele_dic.keys()[0])].append(a)
            if dic_temp[(idlist[k].keys()[0],ele_dic.keys()[0])] != []:
                pairlist.append(dic_temp)

keylist = []
for elem in pairlist:
    if elem.keys()[0][0] not in keylist:
        keylist.append(elem.keys()[0][0])
    if elem.keys()[0][1] not in keylist:
        keylist.append(elem.keys()[0][1])
keylist = list(set(keylist))

sourcelable = {}
for item in range(len(keylist)):
    sourcelable[item] = keylist[item]
sourcelable = {v: k for k, v in sourcelable.items()}

CAID = []
for sth in CAlist:
    for eve in sourcelable:
        if eve in sth.keys():
            CAID.append(sourcelable[eve])

n = []
for dic_memberid in pairlist:
    k1 = dic_memberid.keys()[0][0]
    k2 = dic_memberid.keys()[0][1]

    dic_memberid[(sourcelable[k1],sourcelable[k2])] = dic_memberid.pop((k1,k2))
    dic_memberid[(sourcelable[k1],sourcelable[k2])] = math.ceil(100*1.0/
                                                      (len(dic_memberid[(sourcelable[k1],sourcelable[k2])])))
    n.append(dic_memberid)

maxmin = []
for i in n:
    maxmin.append(i.values()[0])
#print "max is", max(maxmin)
#print "min is", min(maxmin)
newlist = []
for element in n:
    dic2_temp = {}
    dic2_temp["source"] = element.keys()[0][0]
    dic2_temp["target"] = element.keys()[0][1]
    dic2_temp["value"] = element.values()[0]
    if element.keys()[0][0] in CAID:
        print "is CA"
        dic2_temp['state'] = 2
    else:
        print "is NY"
        dic2_temp['state'] = 1
    newlist.append(dic2_temp)
    newlist.append(dic2_temp)

# need to order newlist by source id
newlist.sort(key=operator.itemgetter('source'))
print "sort new list is",len(newlist)

# Need to assign node based on source and target
# use idname and source table
d_nodes = {}
for z in sourcelable:
    for y in idnameall:
        if z == y.keys()[0]:
            #print "y is", y.values()[0]
            d_nodes[sourcelable[z]] = y.values()[0]

# assign nodes
q = []
for w in d_nodes:
    print "w is", w
    dic3_temp = {}
    dic3_temp['name'] = d_nodes[w]

    if w in CAID:
        print "is CA"
        dic3_temp['group'] = 2
    else:
        print "is NY"
        dic3_temp['group'] = 1
    q.append(dic3_temp)

d = {}
d["nodes"] = q
d["links"] = newlist
with open('d3-NYCA25.json', 'w') as fp:
    json.dump(d, fp, indent=4)
fp.close()







