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
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1806lxh@127.0.0.1/flask_demo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 不显示警告

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db',MigrateCommand)

# 老师对班级,中间表(多对多)
teacher_klass = db.Table('teacher_klass',
                         db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id')),
                         db.Column('klass_id', db.Integer, db.ForeignKey('klass.id'))
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
    klasses = db.relationship('Klass', secondary=teacher_klass, backref=db.backref('teachers', lazy='dynamic'), lazy=True)


@manager.command
def produce_klass():
    '''Python manage.py produce_klass
    传入数据到表中
    '''
    k1 = Klass(name='sz1801', desc='A', number=17)
    k2 = Klass(name='sz1802', desc='A', number=34)
    k3 = Klass(name='sz1803', desc='A', number=34)
    k4 = Klass(name='sz1804', desc='A', number=34)
    k5 = Klass(name='sz1805', desc='A', number=34)
    k6 = Klass(name='sz1806', desc='A', number=34)
    k7 = Klass(name='sz1807', desc='A', number=34)
    k8 = Klass(name='sz1808', desc='A', number=34)
    db.session.add_all([k1,k2,k3,k4,k5,k6,k7,k8])
    db.session.commit()

# 测试用
@app.route('/base/')
def hello():
    return render_template('base.html')

# 首页视图函数,展示所有的班级信息
@app.route('/')
def index():
    klasses = Klass.query.all()
    return render_template('index.html', klasses=klasses)

if __name__ == '__main__':
    manager.run()
    # app.run()

# 初始化数据表
# python manage.py db init
# 没问题就会有个migrations文件

# 迁移生成版本
# python manage.py db migrate

# 生成表
# python manage.py db upgrade
