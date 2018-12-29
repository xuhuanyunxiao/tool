#!/usr/bin/env python
# -*- coding: utf-8 -*-

#%%
'''
命名规则：
1 变量：普通 this_is_a_var、全局 GLOBAL_VAR_NAME
2 包名 & 模块名：package_name、module_name.py
3 函数 & 方法：function_name()、method_name()
4 类名 & 异常：ClassName、ExceptonName
5 常量：MAX_OVERFLOW

模块内容的顺序：
    模块说明和docstring — import — globals&constants — 其他定义;
其中import部分:
    又按标准、三方和自己编写顺序依次排放，之间空一行。
    
使用：
    import toolkits  # toolkits.specific_func.contain_ch('salskdj中文')
    from toolkits.setup.specific_func import set_ch_pd
    
文档测试：
def multiply(a, b):
    """
    >>> multiply(4, 3)
    12
    >>> multiply('a', 3)
    'aaa'
    """
    return a * b

import doctest
doctest.testmod(verbose=True)
'''

#%%
import datetime as dt
import re

import numpy as np
import pandas as pd

from toolkits.nlp.langconv import *

#%% 中文相关
def set_ch_pd():
    '''
    功能：设定绘图时显示中文，pandas 显示
    '''	
    from pylab import mpl
    mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False   # 解决保存图像是负号'-'显示为方块的问题

    pd.set_option('display.max_colwidth',1000) # 显示列数
    pd.set_option('precision', 3) # 设置精度
    pd.set_option('display.float_format', lambda x:'%.3f' %x) # 不采用科学计数法显示

#
def contain_ch(word, pattern = None):
    '''
    Function：
        简单判断传入字符串是否包含中文
    Arguments： 
        word -> string -- 待判断字符串
        pattern -> string -- 搜索模式，默认搜索所有中文：u'[\u4e00-\u9fa5]+'
    Return: 
        match -> ？ -- 可用于判断匹配成功，或失败    
    
    >>> contain_ch('salskdj中文')
    '中文'
    '''
    
    if pattern:
        pattern = pattern
    else :
        pattern = u'[\u4e00-\u9fa5]+'
    
    zh_pattern = re.compile(pattern)
    match = zh_pattern.search(word)
    
    return match # match.group() -- '中文'

def Traditional2Simplified(sentence):
    '''
    将sentence中的繁体字转为简体字
    :param sentence: 待转换的句子
    :return: 将句子中繁体字转换为简体字之后的句子
    '''
    sentence = Converter('zh-hans').convert(sentence)
    return sentence

def Simplified2Traditional(sentence):
    '''
    将sentence中的简体字转为繁体字
    :param sentence: 待转换的句子
    :return: 将句子中简体字转换为繁体字之后的句子
    '''
    sentence = Converter('zh-hant').convert(sentence)
    return sentence

#%% 字符匹配
def find_punctuation(data, pattern = None, add_punc = None, del_punc = None):
    '''
    Function：
        找出各类标点符号，以便替换
    Arguments： 
        data -> pandas Series
        pattern -> string -- 搜索模式，默认搜索所有标点符号和空白字符，为 r'[\w]*'
        add_punc -> string -- 需补充的特殊符号，如 '.,?'
        del_punc -> string -- 不包括的标点符号，以pattern形式给出，如 r'[.]*'
    Return: 
        punctuation -> list -- 匹配到的标点符号，或其他内容     
    
    >>> find_punctuation(pd.Series(['sakljdf123456sfda789','sfd123/;、。，；‘、】【{}''sd']))
    '/;{}‘、。【】，；'    
    '''
    
    if pattern:
        pattern = pattern
    else :
        pattern = r'[\w]*'
    
    t = []
    for x in list(data.unique()):t += list(str(x))
    punctuation = re.sub(pattern,'',"".join(list(np.unique(t))))
    
    if add_punc:
        punctuation = punctuation + add_punc
    
    if del_punc:
        punctuation = re.sub(del_punc,'',punctuation)
    
    return punctuation  

#%% 获取txt文本编码信息
def get_txt_encode(file_path):
    '''
    Function:
        获取txt文档的编码格式
    Arguments:
        file_path -> string -- 文档所在路径
    Return:
        encode -> string -- txt文档的编码格式
    '''
    decode_set = ['utf-8','gb18030','ISO-8859-2','gb2312','gbk', 'ANSI'] # 编码集
    encode = 0
    for k in decode_set:
        try :
            file = open(file_path, 'r', encoding = k).read()
            print('\n\t读取成功： %s \n\t编码方式为： %s' %(file_path, k))
            encode = k
            break
        except :
            continue
    if encode:
        return encode
    else :
        return 'No encode'

#encode = get_txt_encode(file_path)
#fid = open(file_path, encoding= encode)
#users = fid.readlines()
#fid.close()    

#%%       
import os
def get_text(folder_path, text_data, file_name):
    '''
    Function:
        循环读取多个文件夹下，多个TXT文档
    Arguments:
        folder_path -> string -- 文档所在路径
        text_data -> list -- 存放内容的空列表
    Return:
        text_data -> list -- 文档内容
    '''      
    if not os.path.exists(folder_path):
        return
    elif os.path.splitext(folder_path)[1] in ['.txt']:
        name = os.path.basename(folder_path)
        file_name.append(name)
        try :
            ch = pd.DataFrame([open(folder_path, 'r').read()], index = [name])
        except UnicodeDecodeError:
            encode = get_txt_encode(folder_path)
            if encode == 'No encode':
                ch = pd.DataFrame([], index = [name])
                print('\n\t未读取数据：%s' %(folder_path))
            else :
                ch = pd.DataFrame([open(folder_path, 'r', encoding = encode).read()], index = [name])
        except Exception as e:
            print(folder_path)
            print(e)
            
        text_data = pd.concat([text_data,ch],axis = 0)                                               
    elif os.path.isdir(folder_path):
        path_list = os.listdir(folder_path)
        for each_path in path_list:
            text_data, file_name = get_text(folder_path + '\\' + each_path,text_data, file_name)
        
    return text_data, file_name      

## 文本数据
#text_data = pd.DataFrame()
#file_name = []
#folder_path = 'D:\XH\Python_Project\Proj_1\data\TanCorpMinTrain'
#text_data, file_name = get_text(folder_path, text_data, file_name)
#%% 文档测试
#import doctest
#doctest.testmod(verbose=True)

#%%

def get_engine(types):
    '''创建mysql连接'''

    from sqlalchemy import create_engine
    from pandas.io import sql
    if types == 'circ':
        # 保监会
        try :
            DB_CON_STR = 'mysql+pymysql://wisedb:Wi$eWeb123@10.80.88.73:5718/pom?charset=utf8'  
            engine = create_engine(DB_CON_STR, echo=False) 
            sql.execute('show databases', engine)
        except :
            DB_CON_STR = 'mysql+pymysql://wisedb:Wi$eWeb123@47.95.148.133:5718/pom?charset=utf8'  
            engine = create_engine(DB_CON_STR, echo=False) 
            sql.execute('show databases', engine)    
    elif types == 'cbrc':
        # 银监会
        try :
            DB_CON_STR = 'mysql+pymysql://atlas:WiseWeb123@47.93.77.228:5636/pom?charset=utf8'  
            engine = create_engine(DB_CON_STR, echo=False) 
            sql.execute('show databases', engine)
        except :
            DB_CON_STR = 'mysql+pymysql://atlas:WiseWeb123@10.28.205.96:5636/pom?charset=utf8'  
            engine = create_engine(DB_CON_STR, echo=False) 
            sql.execute('show databases', engine)    
    elif types == 'cbirc':
        # 银保监会、人寿、建行、人保
        try:
            DB_CON_STR = 'mysql+pymysql://wisedb:Wi$eWeb321@10.31.149.216:5720/cbrc_circ?charset=utf8' 
            engine = create_engine(DB_CON_STR, echo=False)
            cur = sql.execute('show databases', engine)
        except :
            DB_CON_STR = 'mysql+pymysql://wisedb:Wi$eWeb321@39.107.203.231:5720/cbrc_circ?charset=utf8'  
            engine = create_engine(DB_CON_STR, echo=False)
            cur = sql.execute('show databases', engine)  
    elif types == 'ahyjj':
        # 安徽银监局
        try:
            DB_CON_STR = 'mysql+pymysql://wisedb:Wi$eWeb321@10.31.184.133:5720/ahyjj?charset=utf8' 
            engine = create_engine(DB_CON_STR, echo=False)
            cur = sql.execute('show databases', engine)
        except :
            DB_CON_STR = 'mysql+pymysql://wisedb:Wi$eWeb321@47.94.59.63:5720/ahyjj?charset=utf8'  
            engine = create_engine(DB_CON_STR, echo=False)
            cur = sql.execute('show databases', engine)   
    return engine















