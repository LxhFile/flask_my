# -*- coding:utf-8 -*-
# @TIME     :2018/10/18  20:59
# @AUTHOR   :LXH
# @FILE     :manage
# @EXPLAIN  : 程序运行入口

from flask import Flask, render_template
from flask_script import Manager



app = Flask(__name__)



# manager = Manager(app)

@app.route('/')
def hello():
    return 'ok'



if __name__ == '__main__':
    # manager.run()
    app.run()