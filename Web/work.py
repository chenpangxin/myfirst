# # coding:utf-8
# from flask import Flask,render_template,request,redirect,url_for
# from  flask import Blueprint,render_template
# from pcap_catch import pcap
#
# pcap_work = Blueprint('get_pcap',__name__)
#
# @pcap_work.route('/creat_task', methods=['GET','POST'])
# def createTask():
#
#     if request.method == 'GET':
#         return render_template('create.html')
#     elif request.method == 'POST':
#         if pcap.q1.qsize() < 5:
#             setType = request.form['setType']
#             size = request.form['size']
#             startTime = request.form['startTime']
#             ip = request.form['ip']
#             taskName = request.form['taskName']
#             pcap.write(setType+','+size+','+taskName+','+startTime+','+ip)
#             pcap.main()
#             return redirect(url_for('show.showTask'))
#         else:
#             return 'Can`t Create a Task'
#
#
from client_db import con
import json
def a():
    coll = con()
    o = []
    if 3%15==0:
        print 'ss'
    else:
        print '333'
    # for i in coll.find({"finish": 'Y'}).limit(15):
    #     print i['finish']
    #     s = str(i).replace("'",'"')
    #     o.append(s)
    # print  json.dumps({"a":o})

a()