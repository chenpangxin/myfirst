# --*-- coding:UTF-8 --*--
import os
from pymongo import MongoClient
def con():
    client = MongoClient('172.31.50.236', 27017)
    db = client.admin
    db.authenticate('admin', 'antiy//////')
    return client
def cc():
    s = con().chen
    collection = s.ceshi
    ss = []
    s2 = []
    for i in collection.find():
        i = i.get('name')
        ss.append(i)
    return ss
def conn():
    s = con().chen
    coll = s.ceshi
    return coll
def find():
    s = con().chen
    collection = s.ceshi
    ss = []
    s2 = []
    for i in collection.find():
        i = i.get('name')
        ss.append(i)

    for i in collection.find():
        i = i.get('name')
        s2.append(i)
    return s2,ss
#a , m =find()
#print a[1]




# file_path = u"C:\\Users\\ANTIAN\\Desktop\\规则\\"
# with open(file_path+'a.txt','w')as f:
#
#     f.write('gggg')
# f.close()
# print os.path.exists(file_path)
# f = open(file_path, "w+")
#
# f.close()
