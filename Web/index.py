# coding:utf-8
from  flask import Blueprint,render_template,redirect,url_for,request
import re
test  = Blueprint('test',__name__)
@test.route('/',methods=['GET','POST'])
def index():
    print(request.path)
    print(request.url)
    if request.method == 'POST':
        InNumber = request.form['InNumber']
        InNumber = numsort(InNumber)
        return render_template('hello.html', result=InNumber)
    else:
        return render_template('hello.html')
def numsort(number):
    print (number)
#   tmp=number.split(' *')
    tmp=re.split("\s+",number)
    print (tmp)
    for i in range(len(tmp)):
        tmp[i]=int(tmp[i])
    print (tmp)
    tmp.sort()
    res=""
    for i in tmp:
        res+=(str(i)+" ")
    return res

