# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 10:49:30 2017

@author: xh
"""

#%% -----------------     判断参数
# 当函数的参数不确定时，可以使用*args 和**kwargs，*args 没有key值，**kwargs有key值

if ('specific_func' not in dir()) | ('cal_func' not in dir()):
    from toolkits.setup import specific_func  
    from toolkits.setup import cal_func
# from toolkits.setup.specific_func import set_ch_pd

# 开发模式安装包，可及时更新文件
python setup.py develop

#%% -----------------     修改 logging 文件
File "D:\software\conda\lib\logging\handlers.py", line 113, in rotate
    os.rename(source, dest)
# 修改前
if not callable(self.rotator):
    # Issue 18940: A file may not have been created if delay is True.
    if os.path.exists(source):
        os.rename(source, dest)
else:
    self.rotator(source, dest)

# 修改后
if not callable(self.rotator):
    # Issue 18940: A file may not have been created if delay is True.
    try :
        if os.path.exists(source):
            os.rename(source, dest)
    except :
        pass
else:
    self.rotator(source, dest)


#%% -----------------     
# 在嵌套For循环中，将循环次数多的循环放在内侧，循环次数少的循环放在外侧，其性能会提高；
# 减少循环变量的实例化，其性能也会提高。

#%% -----------------  抛出异常
level = 'There is no data!'
raise Exception("Invalid level!",level) #强制触发异常,并传入两个参数
        # 触发异常后，后面的代码就不会再执行

#%% -----------------     读写文件
f = open('/Users/michael/test.txt', 'r', encoding='gbk')
# 如果文件不存在，open()函数就会抛出一个IOError的错误
f.read() # 一次读取文件的全部内容，Python把内容读到内存，用一个str对象表示
f.readline()  # 可以每次读取一行内容，
f.readlines()  # 一次读取所有内容并按行返回list
f.close()
# 文件使用完毕后必须关闭，因为文件对象会占用操作系统的资源，并且操作系统同一时间能打开的文件数量也是有限的

# 由于文件读写时都有可能产生IOError，一旦出错，后面的f.close()就不会调用。
# 所以，为了保证无论是否出错都能正确地关闭文件，我们可以使用try ... finally来实现
try:
    f = open('/path/to/file', 'r')
    print(f.read())
finally:
    if f:
        f.close()

#但是每次都这么写实在太繁琐，所以，Python引入了with语句来自动帮我们调用close()方法：
with open('/path/to/file', 'r') as f:
    print(f.read())
#这和前面的try ... finally是一样的，但是代码更佳简洁，并且不必调用f.close()方法。

# 如果文件很小，read()一次性读取最方便；
# 如果不能确定文件大小，反复调用read(size)比较保险；
# 如果是配置文件，调用readlines()最方便：
for line in f.readlines():
    print(line.strip()) # 把末尾的'\n'删掉

with open('/Users/michael/test.txt', 'w') as f:
    f.write('Hello, world!')

# 追加内容
# a
# 打开一个文件用于追加（只写），写入内容为str
# 如果该文件已存在，文件指针将会放在文件的结尾，新的内容将会被写入到已有内容之后
# 如果该文件不存在，创建新文件进行写入
file = open('test.txt', 'a')
# 创建一个空文件
file = open('text.txt', 'a')
file.write('aaa')
file.close()
file = open('text.txt')
print(file.read())
file.close()

# -------------  json
with open("data/test_set.json",'w',encoding='utf-8') as json_file:
    json.dump(test_set,json_file,ensure_ascii=False)

with open("data/test_set.json",'r',encoding='utf-8') as json_file:
    test_set=json.load(json_file) 

#%% -----------------     re  ----------------------
import re
grade = re.findall(r'[[一|二|三|四|五|六]+年级]*|[[初|高]+[一|二|三]+]*',folderName)

def etl(s):  
    # 去除标点和特殊字符
    regex = re.compile(r"[^\u4e00-\u9f5aa-zA-Z0-9]")
    s = regex.sub('', s)
    
    # 去除字符串中的数字 s = 'abc123def456ghi789zero0'
    remove_digits = str.maketrans('', '', digits)
    res = s.translate(remove_digits)
    return res

from string import digits 
s = 'abc123def456ghi789zero0'
remove_digits = str.maketrans('', '', digits)
res = s.translate(remove_digits)
# 'abcdefghizero'
print(remove_digits)
res    

contents = 'Copyright&copy;1997-2017bywww.people.com.cn.allrightsreserved'
zhmodel = re.compile(u'[\u4e00-\u9fa5]')    #检查中文
#zhmodel = re.compile(u'[^\u4e00-\u9fa5]')   #检查非中文
# contents = u'（2014）深南法民二初字第280号'
match = zhmodel.search(contents)
if match:
    print(contents)
else:
    print(u'没有包含中文')


# URL 
reobj = re.compile(r'(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?')
sent = reobj.sub("", sent)
# E-mail
reobj = re.compile(r'\w+@([0-9a-zA-Z]+[-0-9a-zA-Z]*)(\.[0-9a-zA-Z]+[-0-9a-zA-Z]*)+')
sent = reobj.sub("", sent)
# IP
reobj = re.compile(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)')
sent = reobj.sub("", sent)
# 
reobj = re.compile(r'<a .*?>(.*?)</a>') 
sent = reobj.sub("", sent)    
# <font color="#FF0000">  </font>
reobj = re.compile(r'(?<=<)[/a-zA-Z0-9 ]+=?[“"#a-zA-Z0-9_]*(?=>)')
# (?# reobj = re.compile(r'(?<=<)[[/a-zA-Z0-9 ]+=?"?[“”#a-zA-Z0-9_]*"?]*(?=>)'))
sent = reobj.sub("", sent)
# （文 徐维建 编辑 孙娟） （专栏作家 聂方义）（记者刘美群）（通讯员 郑浩）
reobj = re.compile(r'(?<=（)[文|专栏作家|记者|通讯员| |微信号]*[\u4e00-\u9fa5 a-z]{0,}(?=）)')
sent = reobj.sub("", sent)
reobj = re.compile(r'[责任编辑|更多关于]+[ ：:\u4e00-\u9fa5]*')
sent = reobj.sub("", sent)
# (图)  (图片) (刘敬元)
reobj = re.compile(r'[(?<=（)|(?<=\()][\u4e00-\u9fa5]{0,3}[(?=）)|(?=))]')
sent = reobj.sub("", sent)
# 身份证号
reobj = re.compile(r'([1-9]\d{5}[12]\d{3}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])\d{3}[0-9xX])')
sent = reobj.sub("", sent)
# 手机号码
reobj = re.compile(r'(86)?(1[34578]\d{9})')
sent = reobj.sub("", sent)
# 固定电话
reobj = re.compile(r'\(?(0\d{2,3})?[) -]?\d{7,8}')
sent = reobj.sub("", sent)
# 日期
#  '2017年04月25日11:25:44'
#  '2017年04月25日11:25'
reobj = re.compile(r'[0-9]{2}[:|：][0-9]{2}[:|：]?[0-9]{0,2}')
match = reobj.search(sent)

#%% -----------------     argparse  ----------------------
# 是python的一个命令行解析包，非常编写可读性非常好的程序
from argparse import Namespace

# Arguments
args = Namespace(
    seed=1234,
    data_file="titanic.csv",
    train_size=0.75,
    test_size=0.25,
    num_epochs=100,
)

# Set seed for reproducability
np.random.seed(args.seed)


#%% -----------------     psutil  ----------------------
# CPU、Memory等信息
import psutil

#%% -----------------     总体
users_count = len(psutil.users())
print('用户数: ', users_count)
for u in psutil.users():print(u)

print('开机时间: ', datetime.datetime.fromtimestamp(psutil.boot_time ()).strftime("%Y-%m-%d %H: %M: %S"))
print('CPU物理个数: ', psutil.cpu_count(logical=False))
print('CPU逻辑个数: ', psutil.cpu_count())
print('系统的CPU利用率: ')
print(psutil.cpu_percent(None))
time.sleep(2) 
print(psutil.cpu_percent(None))

memory = psutil.virtual_memory()
print('内存利用率: ', psutil.virtual_memory().percent)
print("Memory Total: %0.2f G"%(memory.total/1024/1024/1024)) # 总的内存大小
print("Memory Free: %0.2f G "%(memory.free/1024/1024/1024)) # 剩余内存大小
memory_used = memory.total - memory.free
print("Memory Used: %0.2f G "%(memory_used/1024/1024/1024)) 
print("Memory Used percent: %0.2f %% "%(memory_used/memory.total * 100))
print('--------------')
print("Memory Used percent: %0.2f %% "%(memory.percent))

psutil.test() 

#%% -----------------     特定
# 查看系统全部进程
for pnum in psutil.pids():
    p = psutil.Process(pnum)
    print(u"进程名 %-20s  内存利用率 %-18s 进程状态 %-10s 创建时间 %-10s " \
    % (p.name(), p.memory_percent(), p.status(), p.create_time()))

psutil.pids() # 查看系统全部进程
p = psutil.Process(16031)
p.name()      #进程名
p.exe()         #进程的bin路径
p.cwd()        #进程的工作目录绝对路径
p.status()     #进程状态
p.create_time()  #进程创建时间
p.uids()      #进程uid信息
p.gids()      #进程的gid信息
p.cpu_times()    #进程的cpu时间信息,包括user,system两个cpu信息
p.cpu_affinity()  #get进程cpu亲和度,如果要设置cpu亲和度,将cpu号作为参考就好
p.memory_percent()  #进程内存利用率
p.memory_info()    #进程内存rss,vms信息
p.io_counters()    #进程的IO信息,包括读写IO数字及参数
p.connectios()    #返回进程列表
p.num_threads()  #进程开启的线程数

# 听过psutil的Popen方法启动应用程序，可以跟踪程序的相关信息
from subprocess import PIPE
p = psutil.Popen(["/usr/bin/python", "-c", "print('hello')"],stdout=PIPE)
p.name()
p.username()

#%% -----------------     pynvml  ----------------------
# GPU 信息
#python2
pip install nvidia-ml-py2
#python3
pip install nvidia-ml-py3

import pynvml

pynvml.nvmlInit()
print('显示驱动信息: ')
print("Driver: ", pynvml.nvmlSystemGetDriverVersion()) 
print('--------------')
print('设备信息: ')
deviceCount = pynvml.nvmlDeviceGetCount()
print('  共 %s 块 GPU，名称为：'%deviceCount)
for i in range(deviceCount):
    handle = pynvml.nvmlDeviceGetHandleByIndex(i)
    print("    GPU", i, ":", pynvml.nvmlDeviceGetName(handle))
print('--------------')
for i in range(deviceCount):
    print('查看第 %s 块GPU的显存、温度、风扇、电源: '%i)
    handle = pynvml.nvmlDeviceGetHandleByIndex(i)
    info = pynvml.nvmlDeviceGetMemoryInfo(handle)
    print("Memory Total: %0.2f G"%(info.total/1024/1024/1024)) # 总的显存大小
    print("Memory Free: %0.2f G "%(info.free/1024/1024/1024)) # 剩余显存大小
    print("Memory Used: %0.2f G "%(info.used/1024/1024/1024)) 
    print("Memory Used percent: %0.2f %% "%(info.used/info.total*100))
    print("Temperature is %d C"%(pynvml.nvmlDeviceGetTemperature(handle,0)))
    print("Fan speed is ",pynvml.nvmlDeviceGetFanSpeed(handle))
    print("Power ststus",pynvml.nvmlDeviceGetPowerState(handle))
    print('--------------')

#最后要关闭管理工具
pynvml.nvmlShutdown()

#%% -----------------     os  ----------------------
os.listdir(r'c:\windows')
os.getcwd() # 当前工作目录
os.chdir('C:\Users\Python_Folder') # 改变工作目录到dirname
os.curdir # 返回当前工作目录
os.__file__  # D:\envs\py27\lib\os.pyc
os.rename("python26","python21") 
shutil.move("python21","python20") 

os.path.dirname(os.__file__) # 获取路径名  D:\software\Anaconda3\envs\py27\lib
os.path.basename(os.__file__) # 获取文件名  os.pyc
os.path.abspath(os.__file__) # 获得绝对路径   D:\software\Anaconda3\envs\py27\lib\os.pyc
os.path.realpath(os.__file__) #  获取相对路径   D:\software\Anaconda3\envs\py27\lib\os.pyc
os.path.exists('D:\envs\py27\lib') # 路径是否真地存在
os.path.isfile('D:\envs\py27\lib\os.pyc') # 路径是否是一个文件
os.path.isdir('D:\envs\py27\lib') # 路径是否是一个目录
os.path.isabs('D:\envs\py27\lib') # 判断是否是绝对路径

list = os.listdir(rootdir) #列出文件夹下所有的目录与文件

os.path.exists('D:\envs\py27\lib') # 路径是否真地存在
os.path.isfile('D:\envs\py27\lib\os.pyc')  # 路径是否是一个文件
os.path.isdir('D:\envs\py27\lib') # 路径是否是一个目录
os.path.isabs('D:\envs\py27\lib') # 判断是否是绝对路径

if not os.path.exists("python27"):
    os.mkdir("python27")    # 创建单个目录 
if not os.path.exists("python26"):
    os.makedirs(r'python26\test') # 创建多级目录 
if os.path.exists("python27"):
    os.rmdir("python27")    # 只能删除空目录
if os.path.exists("python26"):
    os.removedirs(r'python26\test')   # 删除多个目录    
# 空目录、有内容的目录都可以删 。  
# 递归删除一个目录以及目录内的所有内容
if os.path.exists("python25"):
    shutil.rmtree("python25") 

os.path.split('D:\software\Anaconda3\envs\py27\lib') # 分离目录名
os.path.split('D:\software\Anaconda3\envs\py27\lib\os.pyc') # 分离文件名 
os.path.splitext('D:\software\Anaconda3\envs\py27\lib\os.py') # 分离扩展名
# ('D:\\software\\Anaconda3\\envs\\py27\\lib\\os', '.py')
os.path.splitdrive('D:\software\Anaconda3\envs\py27\lib\os.pyc')  #分离磁盘驱动器
os.path.join("D:\software\Anaconda3\envs\py27\lib","os.pyc")  # 连接目录与文件名或目录
os.path.normpath(path)    # 规范path字符串形式

# os.walk(top[, topdown=True[, onerror=None[, followlinks=False]]])
# topdown --可选，为 True，则优先遍历 top 目录，否则优先遍历 top 的子目录(默认为开启)。
# 如果 topdown 参数为 True，walk 会遍历top文件夹，与top 文件夹中每一个子目录。
for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        print(os.path.join(root, name))
    for name in dirs:
        print(os.path.join(root, name))
#root 所指的是当前正在遍历的这个文件夹的本身的地址
#dirs 是一个 list ，内容是该文件夹中所有的目录的名字(不包括子目录)
#files 同样是 list , 内容是该文件夹中所有的文件(不包括子目录)



#%% -----------------     sys  ----------------------

names = locals()
names['%s' %table_n].to_csv(file_name, index = False, encoding = 'utf-8')

#%% --- 
import os,sys

if __name__=="__main__":

    print( "__file__=%s" % __file__)
    print( "os.path.realpath(__file__)=%s" % os.path.realpath(__file__))
    
    print( "os.path.dirname(os.path.realpath(__file__))=%s" % os.path.dirname(os.path.realpath(__file__)))
    
    print( "os.path.split(os.path.realpath(__file__))=%s" % os.path.split(os.path.realpath(__file__))[0])
    print( "os.path.abspath(__file__)=%s" % os.path.abspath(__file__))
    print( "os.getcwd()=%s" % os.getcwd())
    print( "sys.path[0]=%s" % sys.path[0])
    print( "sys.argv[0]=%s" % sys.argv[0])


#__file__=D:/XH/win_to_centos7/proj_3_score/package/test2.py
#os.path.realpath(__file__)=D:\XH\win_to_centos7\proj_3_score\package\test2.py
#os.path.dirname(os.path.realpath(__file__))=D:\XH\win_to_centos7\proj_3_score\package
#os.path.split(os.path.realpath(__file__))=D:\XH\win_to_centos7\proj_3_score\package
#os.path.abspath(__file__)=D:\XH\win_to_centos7\proj_3_score\package\test2.py
#os.getcwd()=D:\XH\win_to_centos7\proj_3_score\package
#sys.path[0]=
#sys.argv[0]=D:/XH/win_to_centos7/proj_3_score/package/test2.py

# 添加默认模块搜索路径
import sys
sys.path
sys.path.append("c:\\")


#%% --- 
## basestring 问题
try:
    unicode = unicode
except NameError:
    # 'unicode' is undefined, must be Python 3
    str = str
    unicode = str
    bytes = bytes
    basestring = (str,bytes)
else:
    # 'unicode' exists, must be Python 2
    str = str
    unicode = unicode
    bytes = str
    basestring = basestring

