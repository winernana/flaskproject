import uuid

from flask import Blueprint, render_template, abort, request, make_response, Response, redirect, url_for

blue = Blueprint('simple_page', __name__)

# 包内的文件关联（正常情况下无法正确关联）
# 借助第三方插件有序关联(flask-blueprint蓝图）

# @blue.route('/')
@blue.route('/home/')
@blue.route('/www/')
def hello_world():
    return 'Hello World|good!'

###路径参数（默认是string类型）
# 上下参数一一对应
@blue.route('/sss/<name>/')
def sss(name):
    return '名字：'+ name

@blue.route('/qqq/<int:age>/')
def qqq(age):
    print(type(age))
    return '年龄：' + str(age)

@blue.route('/ccc/<float:s>/')
def ccc(s):
    return '成绩：' + str(s)

@blue.route('/sum/<int:a>/<int:b>/<int:c>/')
def sum(a,b,c):
    return '{} + {} + {} = {}'.format(a,b,c,(a+b+c))


@blue.route('/uu/<uuid:u>/')
def uu(u):
    return '登陆成功'
@blue.route('/get/')
def get():
    return str(uuid.uuid4())

@blue.route('/ttt/<any(a,b,c):op>/')
def ttt(op):
    return '套餐类型' + op

@blue.route('/ppp/<path:where>/')
def ppp(where):
    return '我的位置'+ where

####请求类型
@blue.route('/methodtest/',methods=['GET','POST'])
def methodtest():
    return '请求方法测试'


##Request  请求对象
@blue.route('/requesttest/',methods=['GET','POST'])
def requesttest():
    data={
        '请求方式':request.method,
        '请求路径':request.path,
        '请求url':request.url,
        'GET请求参数':request.args,
        'POST请求参数':request.form,
        '文件参数':request.files,
        'cookie':request.cookies,
    }
    return str(data)

##Response响应
@blue.route('/responsetest/')
def responsetest():
    # return 'hello'
    # return 'hello',300

    # temp = render_template('responsetest.html')
    # print(type(temp))
    # return temp

    # response = make_response('hello')

    # temp = render_template('responsetest.html')
    # response = make_response(temp)
    # print(type(response))

    # response = Response('hello')
    # response = Response('hello',404)

    # 重定向
    # response = redirect('/requesttest/')

    # 反向解析（得到的是路由）
    # 用法： url_for('蓝图名.视图名')
    url_path = url_for('simple_page.requesttest')
    response = redirect(url_path)
    return response

##抛出异常
@blue.route('/errtest/')
def errtest():
    # abort(403)
    abort(500)

#异常捕获
@blue.errorhandler(403)
def err403(err):
    return '你来捕获我啊'

@blue.errorhandler(500)
def err500(err):
    return '不服来战'


##状态保持 cookie
@blue.route('/')
def index():
    # 状态保持，然后获取数据
    name = request.cookies.get('username','未登录')
    age = 30
    return render_template('index.html',name=name,age = age)

@blue.route('/login/',methods=['GET','POST'])
def login():
    # 状态保持，然后获取数据
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        # 状态保持
        name = request.form.get('username')
        response = redirect(url_for('simple_page.index'))
        response.set_cookie('username',name,max_age=60*60)


        return response

@blue.route('/register/',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    elif request.method == 'POST':
        name = request.form.get('username')

        print(name)

        # 状态保持
        response = redirect(url_for('simple_page.index'))
        # 设置cookie
        response.set_cookie('username',name,max_age=60*60)

        # 反向解析，重回首页
        return response



@blue.route('/logout/')
def logout():
    response = redirect(url_for('simple_page.index'))
    response.delete_cookie('username')
    return response