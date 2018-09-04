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
    from toolkits.specific_func import set_ch_pd
    
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
from sqlalchemy import create_engine
from pandas.io import sql
#import pandas as pd

#%%
def get_mysql_conn(db_source, db_name ):
    '''
    Function：
        获取mysql的conn
    Arguments： 
        db_source -> string -- 数据库来源，旧平台的保监会（circ）、银监会（cbrc），
                                新平台的银保监会及人寿、建行（cbirc）
        db_name -> string -- 数据库名称
    Return: 
        engine -> ？ -- 返回engine    
    '''
    if db_source == 'circ': # 保监会
        try :
            DB_CON_STR = 'mysql+pymysql://wisedb:Wi$eWeb123@10.80.88.73:5718/{0}?charset=utf8'.format(db_name)  
            engine = create_engine(DB_CON_STR, echo=False) 
            sql.execute('show databases', engine)
        except :
            DB_CON_STR = 'mysql+pymysql://wisedb:Wi$eWeb123@47.95.148.133:5718/{0}?charset=utf8'.format(db_name)    
            engine = create_engine(DB_CON_STR, echo=False) 
            sql.execute('show databases', engine)   
    elif db_source == 'cbrc': # 银监会
        try :
            DB_CON_STR = 'mysql+pymysql://atlas:WiseWeb123@47.93.77.228:5636/{0}?charset=utf8'.format(db_name)    
            engine = create_engine(DB_CON_STR, echo=False) 
            sql.execute('show databases', engine)
        except :
            DB_CON_STR = 'mysql+pymysql://atlas:WiseWeb123@10.28.205.96:5636/{0}?charset=utf8'.format(db_name)    
            engine = create_engine(DB_CON_STR, echo=False) 
            sql.execute('show databases', engine)
    elif db_source == 'cbirc':  # 银保监会、人寿、建行        
        try:
            DB_CON_STR = 'mysql+pymysql://wisedb:Wi$eWeb321@10.31.149.216:5720/{0}?charset=utf8'.format(db_name)   
            engine = create_engine(DB_CON_STR, echo=False)
            sql.execute('show databases', engine)
        except :
            DB_CON_STR = 'mysql+pymysql://wisedb:Wi$eWeb321@39.107.203.231:5720/{0}?charset=utf8'.format(db_name)    
            engine = create_engine(DB_CON_STR, echo=False)
            sql.execute('show databases', engine)
    else :
        engine = 'ERROR： 没有对应mysql数据库'
    
    return engine












