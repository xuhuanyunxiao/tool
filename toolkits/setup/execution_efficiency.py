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

import time
from functools import wraps
 
def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print ("Total time running %s: %s seconds" %
                (function.__name__, str(t1-t0)))
        
        return result
    return function_timer


import random

@profile
def random_sort2(n):
    l = [random.random() for i in range(n)]
    l.sort()
    return l
 
if __name__ == "__main__":
    random_sort2(2000000)

