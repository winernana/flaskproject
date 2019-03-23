from flask import Flask, render_template
from flask_script import Manager


# 实例化对象
app = Flask(__name__)
# 初始化对象
manager = Manager(app)

@app.route('/')   #路由
def hello_world():   #试图函数
    return 'Hello flask!'
@app.route('/home/')
def home():
    return "首页|home"

@app.route('/cart/')
def cart():
    return render_template('cart.html')


if __name__ == '__main__':
    manager.run()
