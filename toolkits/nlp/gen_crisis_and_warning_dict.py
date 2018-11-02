#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
生成预警分类词（危机分类词）：
保险业：保监会危机分类-预警词
银行业：银监会预警分类-预警词
'''

#%%
import json
import pandas as pd
import os


#%% 保险业
file_path = r'crisis_and_warning_dict\保监会危机分类-预警词'
filename_list = os.listdir(file_path)

circ_crisis_dict = {}
circ_crisis = set()
exist_class = []
for filename in filename_list:
    print('-- ', filename)
    class_name = filename.split('.')[0]
    tmp_data = pd.read_excel(file_path + '\\' + filename, header = None)
    if class_name not in circ_crisis_dict:
        circ_crisis_dict[class_name] = []
    for value in tmp_data.loc[:, 0].tolist():
        circ_crisis_dict[class_name].append(value)
        circ_crisis.add(value)
#        if value not in circ_crisis_dict:
#            circ_crisis_dict[value] = class_name
            
#        else :
#            exist_class.append([value, class_name, circ_crisis_dict[value]])
#            print(value, class_name)
#            print('已存在：', circ_crisis_dict[value])

#exist_class = pd.DataFrame(exist_class, columns = ['word', '类别2', '类别1（已存在）'])
#exist_class = exist_class.sort_values(by  = 'word')

file_path = "corpus/circ_crisis_dict.txt"
f = open(file_path, "w+", encoding='UTF-8')
for line in circ_crisis:
    f.write(line + '\n')
f.close() 

with open(file_path.replace('txt', 'json'),'w',encoding='utf-8') as json_file:
    json.dump(circ_crisis_dict,json_file,ensure_ascii=False)
    
#%% 银行业
file_path = r'crisis_and_warning_dict\银监会预警分类-预警词'
filename_list = os.listdir(file_path)

cbrc_warning_dict = {}
cbrc_warning = set()
exist_class = []
for filename in filename_list:
    print('-- ', filename)
    class_name = filename.split('.')[0]
    tmp_data = pd.read_excel(file_path + '\\' + filename, header = None)
    if class_name not in cbrc_warning_dict:
        cbrc_warning_dict[class_name] = []
    for value in tmp_data.loc[:, 0].tolist():
        cbrc_warning_dict[class_name].append(value)
        cbrc_warning.add(value)
#        if value not in circ_crisis_dict:
#            circ_crisis_dict[value] = class_name
            
#        else :
#            exist_class.append([value, class_name, circ_crisis_dict[value]])
#            print(value, class_name)
#            print('已存在：', circ_crisis_dict[value])

#exist_class = pd.DataFrame(exist_class, columns = ['word', '类别2', '类别1（已存在）'])
#exist_class = exist_class.sort_values(by  = 'word')

file_path = "corpus/cbrc_warning_dict.txt"
f = open(file_path, "w+", encoding='UTF-8')
for line in cbrc_warning:
    f.write(line + '\n')
f.close() 

with open(file_path.replace('txt', 'json'),'w',encoding='utf-8') as json_file:
    json.dump(cbrc_warning_dict,json_file,ensure_ascii=False)


#%%

