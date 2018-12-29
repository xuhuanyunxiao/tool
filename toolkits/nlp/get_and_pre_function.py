#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xlrd
import datetime
import numpy as np
import pandas as pd
from toolkits.nlp import pre_cor_circ
from toolkits.nlp import pre_cor_cbrc
from toolkits.setup.specific_func import contain_ch, set_ch_pd
set_ch_pd()
from sklearn import metrics

def predict_right(folder, file_list):
    '''预测正确数据'''
    right_data = pd.DataFrame()
    for file_name in file_list:
        currentPath  = '{0}/{1}'.format(folder, file_name)
        excel = xlrd.open_workbook(currentPath)
        sheet_names = [sheet.name for sheet in excel.sheets()]
        for sheet_name in sheet_names:    
            tmp_data = pd.read_excel(currentPath, sheet_name)
    #         tmp_data = tmp_data[tmp_data['R_W'] == 'Right']
            print('去空值前： ', tmp_data.shape, file_name, sheet_name)
#             tmp_data = tmp_data[tmp_data['备注'] != '删除']
    #         tmp_data = tmp_data.dropna(subset = ['raw_title'], axis = 0)
#             print('去空值后： ', tmp_data.shape, file_name, sheet_name)
            right_data = pd.concat([right_data, tmp_data], axis = 0)    
    return right_data

def correct_wrong_data(folder, file_list):
    '''预测错误修正后数据'''
    correct_wrong_data = pd.DataFrame()
    for file_name in file_list:
        currentPath  = '{0}/{1}'.format(folder, file_name)
        excel = xlrd.open_workbook(currentPath)
        sheet_names = [sheet.name for sheet in excel.sheets()]
        for sheet_name in sheet_names:    
            tmp_data = pd.read_excel(currentPath, sheet_name)
    #         tmp_data = tmp_data[tmp_data['R_W'] == 'Wrong']
            print('去删除前： ', tmp_data.shape, file_name, sheet_name)
            tmp_data = tmp_data[tmp_data['备注'] != '删除']
            tmp_data['备注'] =tmp_data['备注'].astype(str)
    #         tmp_data = tmp_data.dropna(subset = ['raw_title'], axis = 0)
            print('去删除后： ', tmp_data.shape, file_name, sheet_name)

            tmp_data['人工判断'] = tmp_data.apply(lambda x:1 if x['label'] == x['备注'] else 0, axis = 1)
            tmp_data['算法判断'] = tmp_data.apply(lambda x:1 if x['predict_label'] == x['备注'] else 0, axis = 1)
            print('人工误判率： %0.2f'%(1 - tmp_data['人工判断'].sum() / tmp_data.shape[0]),
                  '算法误判率： %0.2f'%(1 - tmp_data['算法判断'].sum() / tmp_data.shape[0]))
            print()

            correct_wrong_data = pd.concat([correct_wrong_data, tmp_data], axis = 0)
    return correct_wrong_data

def get_new_data(folder, file_list):
    '''新补充数据'''
    new_data = pd.DataFrame()
    for file_name in file_list:
        currentPath  = '{0}/{1}'.format(folder, file_name)
        excel = xlrd.open_workbook(currentPath)
        sheet_names = [sheet.name for sheet in excel.sheets()]
        for sheet_name in sheet_names:    
            tmp_data = pd.read_excel(currentPath, sheet_name)
            print(tmp_data.columns)
            tmp_data = tmp_data[['label', 'title', 'content']]
            tmp_data['label'] =tmp_data['label'].astype(str)
            tmp_data = tmp_data[tmp_data['label'] != '删除']
            print('去空值前： ', tmp_data.shape, file_name, sheet_name)
            tmp_data = tmp_data.dropna(subset = ['label'], axis = 0)
            print('去空值后： ', tmp_data.shape, file_name, sheet_name)
            new_data = pd.concat([new_data, tmp_data], axis = 0)    
    return new_data

def get_PR_plot_data(feedback_data, date, plot_data, key_col):
    y_pred_class = feedback_data[feedback_data['date'] == date][key_col].astype(str).tolist()
    y_test = feedback_data[feedback_data['date'] == date]['label'].astype(str).tolist()
    print('accuracy_score: ', metrics.accuracy_score(y_test, y_pred_class)) # 指所有分类正确的百分比
    print(metrics.classification_report(y_test, y_pred_class))
    print('confusion_matrix: ')
    print( metrics.confusion_matrix(y_test, y_pred_class))
    print()       
    
    classification_report = metrics.classification_report(y_test, y_pred_class)
    lines = classification_report.split('\n')
    # plot_data = []
    avg_list = ['micro_avg', 'macro_avg', 'weighted_avg']
    a = 0
    for index, line in enumerate(lines[2 : len(lines)]):
        t = line.strip().split()
        if len(t) < 2: continue    
        if (index + 2) < (len(lines) - 4):
            t = [float(v) if i > 0 else v for i, v in enumerate(t)]
            plot_data.append(t + [date])
        else :
            t = [float(v) if i > 1 else v for i, v in enumerate(t) ]
            plot_data.append([avg_list[a]] + t[2:] + [date])  
            a = a + 1 
            
    return plot_data

def get_feedback_data(folder, file_list, key_col):
    '''模型预测后反馈数据'''
    feedback_data = pd.DataFrame()
    label_list = []
    sum_list = []
    right_list = []
    plot_data = []
    for file_name in file_list:
        print('  ----    ', file_name)
        date = file_name.split('_')[0]
        currentPath  = '{0}/{1}'.format(folder, file_name)
        excel = xlrd.open_workbook(currentPath)
        sheet_names = [sheet.name for sheet in excel.sheets()]
        for sheet_name in sheet_names:   
            tmp_data = pd.read_excel(currentPath, sheet_name)    
            tmp_data['label'] =tmp_data['label'].astype(str)
            tmp_data = tmp_data[tmp_data['label'] != '删除']
            tmp_data_1 = tmp_data[tmp_data['label'] == sheet_name]

            label_list.append(sheet_name)
            sum_list.append(tmp_data.shape[0])
            right_list.append(tmp_data_1.shape[0])
            print('类别：', sheet_name, '总数：', tmp_data.shape[0], 
                  '正确数', tmp_data_1.shape[0], 
                  '正确比例', tmp_data_1.shape[0]/tmp_data.shape[0])
            
            if key_col in tmp_data_1.columns:
                tmp_data_1 = tmp_data[[key_col, 'label', 'title', 'content']]
            else :
                tmp_data_1 = tmp_data[['label', 'title', 'content']]
                if contain_ch(sheet_name) :
                    tmp_data_1['predict_label'] = sheet_name
                else :
                    tmp_data_1['predict_label'] = ''
                
            tmp_data_1['date'] = date
            print('去空值前： ', tmp_data_1.shape, file_name, sheet_name)
            tmp_data_1 = tmp_data_1.dropna(subset = ['label'], axis = 0)
            print('去空值后： ', tmp_data_1.shape, file_name, sheet_name)
            feedback_data = pd.concat([feedback_data, tmp_data_1], axis = 0)
            print() 
                        
        plot_data = get_PR_plot_data(feedback_data, date, plot_data, key_col) 
            
    PR_data = feedback_data[['date', key_col, 'label']]
    feedback_data = feedback_data.drop('date', axis = 1)
    feedback_data = feedback_data.drop(key_col, axis = 1)
    PR_plot_data  = pd.DataFrame(plot_data, columns = ['label', 'precision', 'recall', 
                                                    'f1-score', 'support', 'date'])     
    
    return feedback_data, PR_data, PR_plot_data

def pre_save(pre_func, data, save_folder):
    print(data.shape)
    print('save_folder: ', save_folder)
    
    titles = pre_func(data['title'].tolist())
    print('title num: ', len(titles))
    save_filename = save_folder + 'titles.txt'
    fid = open(save_filename, "w+", encoding='UTF-8')
    for line in titles:
        fid.write(line + '\n')
    fid.close()  
    
#     print(len(data['content'].tolist()))
    contents = pre_func(data['content'].tolist())
    print('content num: ', len(contents))
    print(contents[0])
    # contents = [re.sub(r'[a-z]*', '', x) for x in contents]
    # print(len(contents))
    # print(contents[:2])
    coprus_save_filename = save_folder + 'contents.txt'
    f = open(coprus_save_filename, "w+", encoding='UTF-8')
    for line in contents:
        f.write(line + '\n')
    f.close()    

    label = data['label'].tolist()
    print('label num: ', len(label))
    coprus_save_filename = save_folder + 'labels.txt'
    f = open(coprus_save_filename, "w+", encoding='UTF-8')
    for line in label:
        f.write(str(line) + '\n')
    f.close()

    data.to_excel(save_folder + 'title_content_label.xlsx', index = False)
    print(save_folder + 'title_content_label.xlsx')
    