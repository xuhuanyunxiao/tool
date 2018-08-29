# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 10:49:30 2017

@author: xh
"""

### 
# 在嵌套For循环中，将循环次数多的循环放在内侧，循环次数少的循环放在外侧，其性能会提高；
# 减少循环变量的实例化，其性能也会提高。

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

#--  json
with open("data/test_set.json",'w',encoding='utf-8') as json_file:
    json.dump(test_set,json_file,ensure_ascii=False)

with open("data/test_set.json",'r',encoding='utf-8') as json_file:
    test_set=json.load(json_file)    

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

#%% --- 




