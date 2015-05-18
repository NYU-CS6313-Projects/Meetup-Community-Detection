import json
import random
import math
import operator
from collections import Counter
from collections import OrderedDict

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
            if i["state"] == "NJ":
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
                if i['topics'] != []:
                    for e in i['topics']:
                        topics.append(e["name"])
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
                if i['topics'] !=[]:
                    for e1 in i['topics']:
                        topics1.append(e1["name"])
                idd1 = {}
                idd1[i['id']] = topics1
                if idd1[i['id']] != []:
                    idlist1.append(idd1)

        l.append(dict)
        l1.append(dict1)

idnameall = idname+idname1
print "name", idnameall
allidlist = idlist+idlist1

# random sample same number of data points from NY and CA
CAlist = random.sample(idlist,45)
NYlist = random.sample(idlist1,45)
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
    keylist.append(elem.keys()[0][0])
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

# get interests of a single member
member_int = []
c = 0
for itemes in idlist:
    key_old = itemes.keys()[0]
    if key_old in keylist:
        c+=1
        itemes[sourcelable[key_old]] = itemes.values()[0]
        del itemes[key_old]
        #print "new items",itemes
        member_int.append(itemes)

n = []
for dic_memberid in pairlist:
    k1 = dic_memberid.keys()[0][0]
    k2 = dic_memberid.keys()[0][1]
    dic_memberid[(sourcelable[k1],sourcelable[k2])] = dic_memberid.pop((k1,k2))
    dic_memberid[(sourcelable[k1],sourcelable[k2])].append( math.ceil(100*1.0/
                                                      (len(dic_memberid[(sourcelable[k1],sourcelable[k2])]))))

    n.append(dic_memberid)
# print "n is here",n
# get interest overlap range:
oevrlap_range = []
for i in n:
    oevrlap_range.append(math.ceil(1/(i.values()[0][-1]/100)))
# print "max is", max(oevrlap_range)
# print "min is", min(oevrlap_range)
maxmin = []
for i in n:
    maxmin.append(i.values()[0])
#print "max is", max(maxmin)
#print "min is", min(maxmin)
#print "CAID id", CAID
newlist = []
for element in n:
    #print "element is",element
    dic2_temp = {}
    dic2_temp["source"] = element.keys()[0][0]
    dic2_temp["target"] = element.keys()[0][1]
    dic2_temp["value"] = element.values()[0][-1]
    dic2_temp["common_interest"] = element.values()[0][:-1]
    if element.keys()[0][0] in CAID:
        #print "is CA"
        dic2_temp['state'] = 2
    else:
        #print "is NY"
        dic2_temp['state'] = 1
    newlist.append(dic2_temp)
#print "old newlist is", newlist

# need to order newlist by source id
newlist.sort(key=operator.itemgetter('source'))
# print "sort new list is",newlist

# New list creates the source, target ,value format of data.
# need to count how many dots is one node connected to
connect = []
count = 0
for it in range(len(newlist)-1):
    #print "check count", count
    a = newlist[it]['source']
    if newlist[it+1]['source'] == a:
        count+=1
    else:
        d_connect = {}
        d_connect['source'] = a
        d_connect['connect_to'] = count
        connect.append(d_connect)
        count = 0
# print "connect", connect


# Need to assign node based on source and target
# use idname and source table
d_nodes = {}
for z in sourcelable:
    for y in idnameall:
        if z == y.keys()[0]:
            #print "y is", sourcelable[z]
            d_nodes[sourcelable[z]] = y.values()[0]

# assign nodes
q = []
for w in d_nodes:
    #print "w is", w
    dic3_temp = {}
    dic3_temp['name'] = d_nodes[w]
    for z in member_int:
        #print "zkeys is", z.keys()[0]
        if w == z.keys()[0]:
            dic3_temp['interests'] = z.values()[0]
            dic3_temp['number_of_interests'] = len(z.values()[0])
    if w in CAID:
        # print "is CA"
        dic3_temp['group'] = 2
    else:
        #print "is NY"
        dic3_temp['group'] = 1
    # add connect_to key to dictionary
    for h in connect:
        if w == h['source']:
            dic3_temp['connect_to'] = h['connect_to']
    q.append(dic3_temp)
#print "q is",q

# Need to create the list of top ten interests and write to a file
topic_list = []
# print "member interests", member_int
for instance in member_int:
    topic_list+= instance.values()[0]
#print Counter(topic_list)
intlist_sort = sorted(Counter(topic_list).items(),key=lambda x: x[1],reverse=True)

# Create d3 data format to store the top ten interests and the occurences
toptenint = {}
xiao = []
for ins in intlist_sort[:10]:
    d_xiao = {}
    d_xiao[ins[0]] = ins[1]
    xiao.append(d_xiao)
toptenint["topteninterests"] = xiao
#print "toptne interst", toptenint
#print len(xiao)

with open('d3-NYNJ45_intlist.json', 'w') as file:
    json.dump(toptenint, file, indent=4)
file.close()

d = {}
d["nodes"] = q
d["links"] = newlist
with open('d3-NYNJ45_try.json', 'w') as fp:
    json.dump(d, fp, indent=4)
fp.close()




