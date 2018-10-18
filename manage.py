# -*- coding:utf-8 -*-
# @TIME     :2018/10/18  20:59
# @AUTHOR   :LXH
# @FILE     :manage
# @EXPLAIN  : 程序运行入口
import os

from flask import Flask, render_template
from flask_script import Manager, Shell # 控制脚本
from flask_sqlalchemy import SQLAlchemy # sql 点金术  基类数据库
from flask_migrate import Migrate, MigrateCommand


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1806lxh@127.0.0.1/flask_demo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 不显示警告

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command(db,MigrateCommand)

# 老师对班级,中间表(多对多)
teacher_klass = db.Table('teacher_klass',
                         db.Column('teacher_id', db.Integer, db.ForeignKey('teacher_id')),
                         db.Column('klass_id', db.Integer, db.ForeignKey('klass_id'))
                         )

class Klass(db.Model):
    '''
    id : 班级id
    name : 班级名称
    desc : 班级详情
    number : 班级人数
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    desc = db.Column(db.Text)
    number = db.Column(db.SmallInteger)
    def __repr__(self):
        return f'<klass {self.name}>'

class Teacher(db.Model):
    '''
    id : 老师工号
    name : 老师名字
    klass : 老师任教班级
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), nullable=False)
    klasses = db.relationship('Klass', secondary=teacher_klass, backref=db.backref('teachers'))


@manager.command
def produce_klass():
    k1 = Klass(name='sz1801', desc='全班留级', number=17)
    k2 = Klass(name='sz1802', desc='非常好', number=34)
    db.session.add_all([k1,k2])
    db.session.commit()


@app.route('/')
def hello():
    return 'ok'

if __name__ == '__main__':
    manager.run()
    # app.run()