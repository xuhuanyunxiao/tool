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
import datetime
import pandas as pd
import numpy as np


#%%
def get_day_list(start, end):
    '''
    Function：
        获取时间范围
    Arguments：
	    start='2018-08-10'
	    end='2018-08-16'
    Return: 
        day_list -> 日期列表，前开后闭   
        
    >>> day_list = get_day_list('2018-08-22', '2018-08-26') # 前开后闭
    ['2018-08-23', '2018-08-24', '2018-08-25', '2018-08-26']
    '''

    datestart=datetime.datetime.strptime(start,'%Y-%m-%d')
    dateend=datetime.datetime.strptime(end,'%Y-%m-%d')

    day_list = []
    while datestart<dateend:
        datestart+=datetime.timedelta(days=1)
        day_list.append(datestart.strftime('%Y-%m-%d'))
        
    return day_list


#if punctuation:
#    for p in list(punctuation):num = num.replace(p,'.')
#%%  获取年份信息
def get_year_value(index,value):
    '''
    Function：
        找出出生日期的年份。如果含中文，返回np.nan
    Arguments：
        index -> str -- value 对应的索引值
        value -> str -- 日期值，如 2017-10-12
    Return: 
        v -> str -- 年份，如 2017    
        
    >>> get_year_value(1,'2017-10-12')
    '2017'
    '''

    try :
        value = str(value)
        if contain_ch(value):
            v = np.nan
        else :
            if value == 'nan':
                v = np.nan
            else :
                if len(value) < 8:
                    if '.' in value:
                        d = pd.TimedeltaIndex(pd.DataFrame([float(value)])[0], unit='d') + dt.datetime(1899, 12, 30)                    
                    else :
                        d = pd.TimedeltaIndex(pd.DataFrame([int(value)])[0], unit='d') + dt.datetime(1899, 12, 30)
                    y = d.year[0]
                    if 1990 < y & y < 2017:
                        v = y
                    else :
                        v = np.nan
                elif len(value) == 8:
                    y = value[:4]
                    if 1900 < int(y) & int(y) < 2017:
                        v = y 
                    else :
                        v = np.nan                    
                else :
                    if value[4] == '/':
                        v= dt.datetime.strptime(str(value), "%Y/%m/%d").year
                    elif value[4] == '-':
                        if ':' in value:
                            v= dt.datetime.strptime(str(value), "%Y-%m-%d %H:%M:%S").year
                        else :
                            v= dt.datetime.strptime(str(value), "%Y-%m-%d").year
                    elif value[4] == '.':
                        v= dt.datetime.strptime(str(value), "%Y.%m.%d").year                            
                    else :
                        v= dt.datetime.strptime(str(value), "%Y%m%d").year
    except Exception as e:
        print(index,value,e)
    return v  