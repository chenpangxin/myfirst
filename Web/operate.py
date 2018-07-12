# coding:utf-8
import subprocess
from flask import Blueprint, render_template,request, redirect, url_for,jsonify
from client_db import con
from pcap_catch import pcap
import json

op = Blueprint('audit', __name__)

@op.route('/caughttask', methods=['GET','POST','PUT','DELETE'])
def createTask():
    coll = con()
    if request.method == 'GET':
        data = request.args
        page = int(data['page'])
        limit = int(data['limit'])
        # number = 5 - int(pcap.q1.qsize())
        # count 表示数据的分页数
        c = coll.find().count()
        if c % 15 == 0:
            count = c / 15
        else:
            count = c / 15 + 1
        if int(page) <= count:
            s = []
            for i in coll.find({"finish": 'N'}).limit(limit).skip((page - 1) * limit):
                s.append(i)
            return json.dumps({'status': 1,'message': 'ok','payload':{'data': s, 'total': count}})
        else:
            return json.dumps({'status': -1, 'message': 'page not exist'})
    elif request.method == 'POST':
        if pcap.q1.qsize() < 5:
            a = json.loads(request.get_data())
            s = []
            name = a['taskName']
            for i in coll.find():
                s.append(i['taskName'])
            if name in s:
                return json.dumps({"status":-1,"message": "name is exist"})
            else:
                setType = a['setType']
                size = a['size']
                startTime = a['startTime']
                ip = a['ip']
                taskName = a['taskName']
                pcap.write(setType+','+size+','+taskName+','+startTime+','+ip)
                pcap.action()
                return json.dumps({"status": 1, "message": "ok"})
        else:
            return json.dumps({"status":-1,"message": "task is full"})
    elif request.method == 'PUT':
        try:
            id = json.loads(request.get_data())['_id']
            for i in coll.find({"_id": int(id)}):
                if i['pid'] == '' and i['status'] == 'TimeError':
                    pass
                elif i['status'] == 'Cancel':
                    pass
                elif i['pid'] == '' and i['status'] == 'Waiting':
                    # 首先判断是否有这个进程pid，不然的话会报错
                    s = subprocess.check_output('pgrep python', shell=True)
                    if str(i['pypid']) in s.split('\n'):
                        subprocess.call('kill -9 ' + str(i['pypid']), shell=True)
                        pcap.q1.get()
                    else:
                        pass
                elif i['pid'] != '':
                    s = subprocess.check_output('pgrep python', shell=True)
                    if str(i['pid']) in s.split('\n'):
                        subprocess.call('kill -9 ' + str(i['pypid']), shell=True)
                        pcap.q1.get()
                    else:
                        pass
            coll.update({"_id": int(id)}, {"$set": {"status": 'Cancel'}})
            return json.dumps({"status": 1, "message": "ok"})
        except:
            return json.dumps({{"status": -1, "message": "Id is no exist"}})
    elif request.method == 'DELETE':
        try:
            id = json.loads(request.get_data())['_id']
            coll.remove({"_id": int(id)})
            return json.dumps({"status": 1, "message": "ok"})
        except:
            return json.dumps({{"status":-1,"message": "Id is no exist"}})

@op.route('/caughtrecord')
def showRecordCount():
    data = request.args
    page = int(data['page'])
    limit = int(data['limit'])
    coll = con()
    c = coll.find({"finish": 'Y'}).count()
    if c % 15 == 0:
        count = c / 15
    else:
        count = c / 15 + 1
    if int(page)<= count:
        s = []
        for i in coll.find().limit(limit).skip((page - 1) * limit):
            s.append(i)
        return json.dumps({'data':s,'total':count})
    else:
        return json.dumps({'status':-1,'message':'page not exit'})




