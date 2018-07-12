# coding:utf-8
from flask import Flask, render_template, request, redirect
from index import test
from login import logintest
from register import registertest

from operate import op

app = Flask(__name__)
app.register_blueprint(test)
app.register_blueprint(logintest)
app.register_blueprint(registertest)
app.register_blueprint(op)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, use_debugger=True)


