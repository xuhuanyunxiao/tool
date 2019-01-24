# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 10:49:30 2017

@author: xh
"""

#%% -----------------     retry  ----------------------
# 用来实现重试的。
# 很多时候我们都需要重试功能，比如写爬虫的时候，有时候就会出现网络问题导致爬取失败，然后就需要重试了，
# 一般我是这样写的（每隔两秒重试一次，共5次）

from retry import retry

@retry(tries=5, delay=2)
def do_something():
    pass

do_something()
# 也就是在函数的定义前，加一句@retry就行了。


#%% -----------------     tqdm  ----------------------
# 是一个快速，可扩展的Python进度条，
# 可以在 Python 长循环中添加一个进度提示信息，
# 用户只需要封装任意的迭代器 tqdm(iterator)。 
from tqdm import tqdm,trange
from time import sleep

for i in tqdm(range(10000)):  
    # do something
    pass  

for i in trange(100):
    #do something
    pass

bar = tqdm(["a", "b", "c", "d"])
for char in pbar:
    pbar.set_description("Processing %s" % char)

# desc可以指定这个循环的的信息，以便区分。上面的set_description(str)和这个应该是一样的。
# leave则表示进度条跑完了之后是否继续保留
for i in tqdm(range(10), desc='1st loop'):
    for j in trange(100, desc='2nd loop', leave=False):
        sleep(0.01)

# 如果要在Jupyter Notebook上面使用，那么要把tqdm换成tqdm_notebook，trange换成tnrange
from tqdm import tnrange, tqdm_notebook 
from time import sleep 
for i in tqdm_notebook(range(10), desc='1st loop'): 
    for j in tnrange(100, desc='2nd loop', leave=False): 
        sleep(0.01)

