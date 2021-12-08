from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
import os, sys
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import re
import datetime, time

from flask import Flask, request, jsonify

secret_key = "57Blocks"
max_time = 300

WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(24), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    birth = db.Column(db.DateTime)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __str__(self):
        return "Users(id='%s')" % self.id

    def set_password(self, password):
        return generate_password_hash(password)

    def check_password(self, hash, password):
        return check_password_hash(hash, password)


@app.route('/')
def hello():
    return jsonify('hello world')


# 注册接口
@app.route("/register", methods=["POST"])
def register():
    # 通过request.values.get取值，在测试环境下可能有取不到值的情况，所以增加request.get_json()
    username = request.values.get('username', None)
    email = request.values.get('email', None)
    password = request.values.get('password', None)

    print(username, email, password)

    # 判空
    if None in [username, email, password]:
        # 当没有取到值时，通过request.get_json()再确认一遍
        try:
            data = request.get_json()
            username = data.get('username', None)
            email = data.get('email', None)
            password = data.get('password', None)
        except:
            pass
        if None in [username, email, password]:
            return jsonify({
                "state": "failed",
                "err_info": "请输入完整数据"
            })

    # 检查邮箱格式
    if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        return jsonify({
            "state": "failed",
            "err_info": "邮箱格式不正确"
        })

    # 判断是否已经注册，如果已经注册，则返回该用户已经注册信息
    if User.query.filter(or_(User.email == email, User.username == username)).first():
        return jsonify({
            "state": "failed",
            "err_info": "该邮箱已经被注册"
        })
    # 如果没有该用户则顺利注册
    else:
        user = User(username=username,
                    password=password,
                    email=email)
        db.session.add(user)
        db.session.commit()

        return jsonify({
            "state": "success",
            "info": "注册成功"
        })


def verify_token(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        try:
            token = request.headers["Authorization"]
            # 去掉头部的Bearer
            if token[:6] == 'Bearer':
                token = token[7:]

            data = jwt.decode(token, secret_key, algorithms=['HS256'])
            kwargs['uid'] = data['uid']
            now = int(time.time())
            time_interval = now - data['time']

            if time_interval >= max_time:
                return jsonify({
                    "state": "failed",
                    "err_info": "Token 已过期"
                })
        except Exception as ex:
            return jsonify({
                "state": "failed",
                "err_info": "Token 已失效，请重新登录"
            })

        return func(*args, **kwargs)

    return decorator


def creat_token(uid):
    now = int(time.time())
    payload = {'uid': uid, 'time': now, 'exp': now + max_time}
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token


# 登录接口
@app.route("/login", methods=["POST"])
def login():
    email = request.values.get('email', None)
    password = request.values.get('password', None)

    # 判空
    if None in [email, password]:
        try:
            data = request.get_json()
            email = data.get('email', None)
            password = data.get('password', None)
        except:
            pass
        if None in [email, password]:
            return jsonify({
                "state": "failed",
                "err_info": "请输入邮箱和密码"
            })

    user = User.query.filter_by(email=email, password=password).first()
    if user:
        token = creat_token(user.id)
        return jsonify({
            "state": "success",
            "token": token
        })
    return jsonify({"state": "failed"})


# 编辑接口
@app.route("/edit", methods=["POST"])
@verify_token
def edit(*args, **kwargs):
    try:
        uid = kwargs['uid']
        user = User.query.filter_by(id=uid).first()

        data = request.get_json()
        username = data.get("username", None)
        age = data.get("age", None)
        birth = data.get("birth", None)

        all_null_flag = True

        if username:
            user.username = username
            all_null_flag = False
        if age:
            user.age = age
            all_null_flag = False
        if birth:
            birth_date = datetime.datetime.strptime(birth, "%Y-%m-%d").date()
            user.birth = birth_date
            all_null_flag = False

        if all_null_flag:
            return jsonify({"state": "failed",
                            "err_info": "缺少参数"})
        else:
            db.session.commit()

        # print打印出结果便于调试与检查
        print("now age:", user.age)
        print("now name:", user.username)
        print("now birth:", user.birth)
        return jsonify({"state": "success"})
    except Exception as e:
        return jsonify({
            "state": "failed",
            "err_info": e
        })
