# coding:utf-8
from flask import Flask,render_template,request,redirect
from  flask import Blueprint,render_template,jsonify
import dbclient
logintest  = Blueprint('logintest',__name__)

@logintest.route('/login',methods=['GET','POST'])
def login():
    l,m = dbclient.find()
    if request.method =='GET':
        return render_template('login.html')
    elif request.method =='POST':
        name = request.form['username']
        pw =request.form['password']
        i = 0
        print len(l)
        while(1):
            if len(l)-1 < i:
                return render_template('error.html')
                break
            if name ==l[i] and pw == m[i]:
                return render_template('success.html', name=request.form['username'])
                break
            else:
                i+=1

