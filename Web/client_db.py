# --*-- coding:UTF-8 --*--
import os
from pymongo import MongoClient
def con():
    client = MongoClient('172.31.50.236', 27017)
    db = client.admin
    db.authenticate('admin', 'antiy//////')
    db2 = client.chen
    coll = db2.ceshi
    return coll