#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 16:37:38 2017

@author: xh
"""
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
    import Tookits  # Tookits.specific_func.contain_ch('salskdj中文')
    from Tookits.specific_func import set_ch
    
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
from itertools import combinations
import time

import pandas as pd
import numpy as np

#%%
def descirbing_feature(feature_data):
    '''
    功能：描述 一个特征/字段 的信息，包括：'是否缺失样本', '缺失量', '缺失率','现存量',
             '缺失样本索引', '该特征含值的个数','值内容','值个数'
    param： 
        feature_data: 特征/字段 数据，pandas Series
    return: 
        pandas Series    
    '''
    
    missing_samples = feature_data[feature_data.isnull()]
    if missing_samples.shape[0] is not 0:   
        exist_missing = 'YES'                      
        missing_samples_size = missing_samples.shape[0]
        missing_samples_rate = missing_samples_size / feature_data.shape[0]
        retain_samples_size = feature_data.shape[0] - missing_samples_size
        missing_samples_index = list(missing_samples.index)
    else:
        exist_missing = 'NO' 
        missing_samples_size = 0
        missing_samples_rate = missing_samples_size / feature_data.shape[0]
        retain_samples_size = feature_data.shape[0] - missing_samples_size
        missing_samples_index = []  
        
    # drop missing value, and find strange value
    clean_data = feature_data.dropna()        
    value_size = clean_data.unique().shape[0]
    value_count = clean_data.value_counts()
    value_count_name = list(value_count.index)
    value_count = list(value_count)
        
    name_list = ['是否缺失样本', '缺失量', '缺失率','现存量',
             '缺失样本索引', '该特征含值的个数','值内容','值个数']  
    
    return pd.Series([exist_missing,missing_samples_size,
                      missing_samples_rate,retain_samples_size,
                      missing_samples_index,value_size,
                      value_count_name,value_count],
                    index = name_list)

#%% 
def describe(data,fea_filename,fea_list = None, sam_filename = None,data_rate = None):
    '''
    功能：1 描述 每个特征/字段 的信息，包括：'是否缺失样本', '缺失量', '缺失率','现存量',
             '缺失样本索引', '该特征含值的个数','值内容','值个数'
          2 选定几个特征做关于频数的透视表
          3 并写入Excel文件中
          4 描述所耗时间
    param： 
        data: 特征/字段 数据，pandas DataFrame
        feas_list: 选定的特征，如 ['年份','年级','性别']
        fea_filename: 描述特征的文件名，完整路径
        sam_filename: 描述选定特征频数的文件名，完整路径
        data_rate：将data中的部分数据写入Excel，方便查看，行总数的比例，如0.1（1%）
    return: 
        写入Excel文件    
    '''
        
    print('--------  描述数据...  ------')
    t0 = time.time()
    
    total_desc = data.describe()
    single_fea_desc = data.apply(descirbing_feature).T
    
#    from line_profiler import LineProfiler
#    import sys
#    
#    prof = LineProfiler(descirbing_feature)
#    prof.enable()  # 开始性能分析
#    describe_data = data.apply(descirbing_feature).T
#    prof.disable()  # 停止性能分析
#    prof.print_stats(sys.stdout)
    
    with pd.ExcelWriter(fea_filename) as writer:
#        total_desc.to_excel(writer,'整体描述')
        single_fea_desc.to_excel(writer,'各个特征')
        if data_rate:
            data.iloc[:int(data.shape[0] * data_rate) + 1,:].to_excel(writer,'部分数据（' + str(data_rate) +')')
        writer.save()
 
    #  describe sample   
    if fea_list:
        data['计数'] = 1    
        for i in np.arange(1,len(fea_list)+1):
            filename = sam_filename + ' ' + str(i) + ' fea.xlsx'
            with pd.ExcelWriter(filename) as writer:
                situations = list(combinations(fea_list, i))
                for fea_name in situations:
    #                G_result = describing_sample(data)
                    G_data = data.groupby(fea_name)['计数']
                    G_result = G_data.count()
                    G_result = G_result.reset_index()
                    G_result.to_excel(writer,'-'.join(list(fea_name)))
                writer.save()
    
    return single_fea_desc
    t1 = time.time() - t0
    print('--------  描述数据.  ------')
    print('--------  耗时（s）：{:0.1f}  ------'.format(t1))

#%%



#%%







