# coding:utf-8
from flask import Flask,render_template,request,redirect
from  flask import Blueprint,render_template
import dbclient
registertest  = Blueprint('registertest',__name__)

# 注册
@registertest.route('/register',methods=['GET','POST'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    elif request.method == 'POST':
        name =request.form['username']
        pw =request.form['password']
        l = dbclient.cc()
        if name =='' or pw =='':
            return render_template('register.html')
        elif name.strip() in l:
            return render_template('error.html')
        else:
            coll = dbclient.conn()
            coll.insert({'name':name.strip(),'password':pw.strip()})
            return redirect('/login')
    return render_template('login.html')