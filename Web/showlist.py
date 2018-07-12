# # coding:utf-8
# from flask import Flask, render_template, request, redirect
# from flask import Blueprint, render_template
# from pcap_db import con
# from pcap_catch import pcap
#
# show = Blueprint('show', __name__)
#
# @show.route('/showrecord')
# def showRecord():
#     coll = con()
#     c = coll.find({"finish": 1}).count()
#     if c % 15 == 0:
#         count = c / 15
#     else:
#         count = c / 15 + 1
#     s = []
#     for i in coll.find({"finish": 1}).limit(15):
#         s.append(i)
#     return render_template('recordlist.html', u=s, count=count)
#
# @show.route('/showrecord/<page>')
# def showRecordCount(page):
#     coll = con()
#     c = coll.find({"finish": 1}).count()
#     if c % 15 == 0:
#         count = c / 15
#     else:
#         count = c / 15 + 1
#     s = []
#     for i in coll.find().limit(15).skip((int(page) - 1) * 15):
#         s.append(i)
#     return render_template('recordlist.html', u=s, count=count)
#
# @show.route('/showtask')
# def showTask():
#     pro = 5 - int(pcap.q1.qsize())
#     coll = con()
#     c = coll.find({"finish": 0}).count()
#     s = []
#     if c % 15 == 0:
#         count = c / 15
#     else:
#         count = c / 15 + 1
#     for o in coll.find({"finish": 0}).limit(15):
#         s.append(o)
#     return render_template('tasklist.html', u=s, count=count, pro=pro)
#
#
# @show.route('/showtask/<page>')
# def showTaskCount(page):
#     pro = 5 - int(pcap.q1.qsize())
#     coll = con()
#     c = coll.find().count()
#     if c % 15 == 0:
#         count = c / 15
#     else:
#         count = c / 15 + 1
#     s = []
#     for i in coll.find({"finish": 0}).limit(15).skip((int(page) - 1) * 15):
#         s.append(i)
#     return render_template('tasklist.html', u=s, count=count, pro=pro)

