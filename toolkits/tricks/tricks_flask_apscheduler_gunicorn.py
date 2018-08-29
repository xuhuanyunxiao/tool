# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 10:49:30 2017

@author: xh
"""

#%% -----------------     服务端 + 客户端  ----------------------
# 服务端代码
from flask import Flask
from flask import request
from flask import Response
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/user/<name>')
def user(name): # get：http://127.0.0.1:5000/user/xh
    return'<h1>hello, %s</h1>' % name

# request.json 只能够接受方法为POST、Body为raw，header 内容为 application/json类型的数据：对应图1
# json.loads(request.dada) 能够同时接受方法为POST、Body为 raw类型的 Text 
# 或者 application/json类型的值：对应图1、2    
@app.route('/my_json', methods=['POST'])
def my_json():
    print(request.headers)
    print(request.json)
    rt = {'info':'hello '+request.json['name']}
    response =Response(json.dumps(rt), mimetype='application/json')
    response.headers.add('Server','python flask')
    #return jsonify({'response':}response)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11000, debug=True) 
    # http://192.168.0.104:11000/index  (启服务的机器IP)
    
    # app.run(host='127.0.0.1', port=5000, debug=True) 
    # http://127.0.0.1:5000/my_json


# 代码启动
# 本地启动：py文件所在文件夹
python file_name.py
# 服务器启动：
/data/anaconda/anaconda3/bin/gunicorn --workers 2 --threads 1 -k gevent --bind 0.0.0.0:10000 --timeout 1800 --error-logfile /data/python_apps/circ/logs/gunicorn.log --log-level debug --capture-output --chdir /data/python_apps/circ --reload --daemon Server_Judge_Correlation1208:app

# 客户端代码
import requests,json

user_info={'name':'letian'}
headers={'content-type':'application/json'}
r = requests.post("http://192.168.0.104:11000/my_json",
                  data = json.dumps(data),
                  headers=headers)
print(r.headers)
print(r.json())  

# 
def get_server_res(data, url):
    '''
    服务器接口测试程序
    传入 dict, 传出 DataFrame
    '''
    # data = {'record':[{'id':0,'title':'ss','content':'zzz'},]}
    # data = {"record":marked_human_data.iloc[:5,:3].to_dict(orient = 'records')}
    # url "http://47.93.77.19:10000/correlation_negative"
    headers={'content-type':'application/json'}
    result = requests.post(url,
                      data = json.dumps(data),
                      headers=headers, allow_redirects=True)
    # print(result.text)
    json_data = json.loads(result.text)
    parse_data = []
    for i in range(len(json_data['docs'])):
        parse_data.append([json_data['docs'][i]['id'],
                          json_data['docs'][i]['sec'],
                          json_data['docs'][i]['tendency']])
    parse_data = pd.DataFrame(parse_data, columns = ['id', 'sec', 'tendency'])    
    return parse_data

# 线上模型
data = {"record":noise_data.loc[:,['id', 'title' ,'content']].to_dict(orient = 'records')}
url = "http://47.93.77.19:10000/correlation_negative"
parse_data = get_server_res(data, url)
res = parse_data['sec'].tolist()
res_3 = 1-float(sum(res))/len(res)
print('%s (%0.3f): '%(day, res_3))

# 保监会
#线上-服务：url = "http://47.93.77.19:10000/correlation_negative"
#线上-测试：url = "http://47.93.77.19:11000/correlation_negative"
#本地-测试：url = "http://192.168.0.104:11000/correlation_negative"

# 银监会
#线上-服务：url = "http://47.93.77.19:10000/correlation_negative"
#线上-测试：url = "http://47.93.77.19:11000/correlation_negative"
#本地-测试：url = "http://192.168.0.104:11000/correlation_negative"


#%% -----------------     flask-apscheduler  ----------------------
# 定时任务
# 官方的GitHub地址：https://github.com/viniciuschiele/flask-apscheduler/blob/master/examples/jobs.py
# 官网例子
from flask import Flask
from flask_apscheduler import APScheduler


class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': 'jobs:job1',  # jobs 文件名：jobs.py
            'args': (1, 2),
            'trigger': 'interval',
            'seconds': 10
        }
    ]

    SCHEDULER_API_ENABLED = True


def job1(a, b):
    print(str(a) + ' ' + str(b))

if __name__ == '__main__':
    app = Flask(__name__)  # 实例化flask
    app.config.from_object(Config())  # 为实例化的flask引入配置

    scheduler = APScheduler()  # 实例化APScheduler
    # it is also possible to enable the API directly
    # scheduler.api_enabled = True   
    scheduler.init_app(app)  # 把任务列表放进flask
    scheduler.start()  # 启动任务列表
    app.run()  # 启动flask

#  ----------------------
class Config(object):
    JOBS = [
            {
               'id':'job1',
               'func':'flask-ap:test_data',
               'args': '',
               'trigger': {
                    'type': 'cron',
                    'day_of_week':"mon-fri",
                    'hour':'0-23',
                    'minute':'0-11',
                    'second': '*/5'
                }
 
             }
        ]

class Config(object):  # 创建配置，用类
    JOBS = [  # 任务列表
        {  # 任务字典（细节）
            'id': 'job1',
            'func': '__main__:print_hello',
            # 'args': (1, 2),
            'trigger': 'cron',
            'hour': 19,
            'minute': 42
        },
        {  # 第二个任务字典
            'id': 'job2',
            'func': '__main__:job_1',
            'args': (3, 4),
            'trigger': 'interval',
            'seconds': 5,
        }
    ]

if trigger_name == 'date':
    trigger_arg_names = ('run_date', 'timezone')
elif trigger_name == 'interval':
    trigger_arg_names = ('weeks', 'days', 'hours', 'minutes', 'seconds', 'start_date', 'end_date', 'timezone')
elif trigger_name == 'cron':
    trigger_arg_names = ('year', 'month', 'day', 'week', 'day_of_week', 'hour', 'minute', 'second', 'start_date', 'end_date', 'timezone')
else:
    raise Exception('Trigger %s is not supported.' % trigger_name)










