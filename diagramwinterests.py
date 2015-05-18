import json
import random
import math
import operator

l = []
idlist = []
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
        dict['group'] = 1
        for e in i['topics']:
            topics.append(e["name"])
        idd = {}
        idd[i['id']] = topics
        if idd[i['id']] != []:
            idlist.append(idd)
        l.append(dict)

# random choose 100 data points
#idlist = idlist[:10]
idlist = random.sample(idlist,20)
#print "idlist",idlist
pairlist = []
for k in range(len(idlist)):
    l_without_k = idlist[(k + 1):]
    kval = idlist[k].values()[0]
    if kval!= []:
        for ele_dic in l_without_k:
            dic_temp = {}
            dic_temp[(idlist[k].keys()[0],ele_dic.keys()[0])] = []
            for a in kval:
                if a in ele_dic.values()[0]:
                    dic_temp[(idlist[k].keys()[0],ele_dic.keys()[0])].append(a)
            if dic_temp[(idlist[k].keys()[0],ele_dic.keys()[0])] != []:
                pairlist.append(dic_temp)
keylist = []
for elem in pairlist:
    keylist.append(elem.keys()[0][0])
    keylist.append(elem.keys()[0][1])
keylist = list(set(keylist))
print "idlist",idlist
print "keylist is",keylist


# commomint = pairlist
# print commomint
# print "pair list is", pairlist
sourcelable = {}
for item in range(len(keylist)):
    sourcelable[item] = keylist[item]
sourcelable = {v: k for k, v in sourcelable.items()}

# get interests of a single member
member_int = []
for itemes in idlist:
    if itemes.keys()[0] in keylist:
        itemes[sourcelable[itemes.keys()[0]]] = itemes.values()[0]
        del itemes[itemes.keys()[0]]
        member_int.append(itemes)
print "member interest", member_int
print len(idlist),len(keylist),len(member_int)
print sourcelable


n = []
for dic_memberid in pairlist:
    k1 = dic_memberid.keys()[0][0]
    k2 = dic_memberid.keys()[0][1]
    dic_memberid[(sourcelable[k1],sourcelable[k2])] = dic_memberid.pop((k1,k2))
    dic_memberid[(sourcelable[k1],sourcelable[k2])].append( math.ceil(100*1.0/
                                                      (len(dic_memberid[(sourcelable[k1],sourcelable[k2])]))))

    n.append(dic_memberid)
print "n is here",n
maxmin = []
# for i in n:
#     maxmin.append(i.values()[0])
# print "max is", max(maxmin)
# print "min is", min(maxmin)
newlist = []
for element in n:
    dic2_temp = {}
    dic2_temp["source"] = element.keys()[0][0]
    dic2_temp["target"] = element.keys()[0][1]
    dic2_temp["value"] = element.values()[0][-1]
    dic2_temp["common_interest"] = element.values()[0][:-1]
    newlist.append(dic2_temp)
print "loooooo",newlist
# Need to order newlist by source id
newlist.sort(key=operator.itemgetter('source'))

# Need to assign node based on source and target
# use idname and source table
d_nodes = {}
for z in sourcelable:
    for y in idname:
        if z == y.keys()[0]:
            d_nodes[sourcelable[z]] = y.values()[0]
print "d nodes",d_nodes
print "idname is", idname
# assign nodes
q = []
for w in d_nodes:
    print "w is", w

    dic3_temp = {}
    dic3_temp['name'] = d_nodes[w]
    dic3_temp['group'] = 1
    for z in member_int:
        if w == z.keys()[0]:
            dic3_temp['interests'] = z.values()[0]
            dic3_temp['number_of_interests'] = len(z.values()[0])



    q.append(dic3_temp)

print "q is", q
d = {}
d["nodes"] = q
d["links"] = newlist
with open('d3int20.json', 'w') as fp:
    json.dump(d, fp, indent=4)
fp.close()



