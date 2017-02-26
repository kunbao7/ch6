# -*- coding:utf-8 -*-
import os
import time
import requests
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['SECRET_KEY'] = '******'


@app.route('/', methods=['GET', 'POST'])
def index():
    weather = ''
    if request.method == 'POST':
        if 'query' in request.form.keys():
            city_name = request.form['city_name']
            weather = get_weather(city_name)
        elif 'history' in request.form.keys():
            history = get_history()
            return render_template('index.html', info=history)
        elif 'help' in request.form.keys():
            help_info = get_help()
            return render_template('index.html', info=help_info)
    return render_template('index.html', info=weather)


# 获取帮助信息
def get_help():
    return ['输入城市名，获取城市天气信息;', '单击帮助按钮，获取帮助文档;', '单击历史按钮，获取查询历史。']


# 历史文件的创建
def history_file():
    if os.path.isfile('history.txt') is False:
        return open('history.txt', 'w', encoding='utf-8')
    else:
        return open('history.txt', 'a+', encoding='utf-8')


# 查询历史
def get_history():
    if os.path.isfile('history.txt') is False:
        return ['您暂未查询任何城市天气信息']
    else:
        history_info = []
        with open('history.txt', 'r', encoding='utf-8') as history:
            for i in history:
                history_info.append(i)
            return history_info


# 查询信息并记录
def get_weather(keyword):

    history = history_file()

    r = requests.get('https://api.thinkpage.cn/v3/weather/now.json?key=r6fdjn8dz8hghngf&location=' + keyword + '&language=zh-Hans&unit=c')

    if r.status_code == 200:
        message_dict = r.json()['results'][0]
        city_name = message_dict['location']['name']
        temperature = message_dict['now']['temperature']
        text = message_dict['now']['text']

        history.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + " " + city_name + " " + text + " " +
                      temperature + '度' + '\n')

        return [city_name + '现在的天气为' + text + ',温度是' + temperature + '度']
    else:
        return ['查询不到您输入的城市天气信息，请重新输入']


# 启动服务器
if __name__ == '__main__':
    app.run(debug=True)
