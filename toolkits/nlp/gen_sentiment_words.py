#!/usr/bin/env python
# -*- coding: utf-8 -*-


#%%
'''
参考论文《基于词典与规则的新闻文本情感倾向性分析》制作各类词典
一、构建词典基础
    1 HowNet_sentiment： http://www.keenage.com/html/c_bulletin_2007.html
    2 台湾大学情感词典
    3 哈工大同义词词林扩展版: synonym.txt
    3 a_level_SP0320.txt

二、词典类型: sentiment_dict
    1 情感词典: emotion_dict
        positive_words：合并中文正面情感词语和中文正面评价词语去重后构建正面基础情感词典
        negative_words：合并中文负面情感词语和中文负面评价词语去重后构建负面基础情感词典
        以 How Net 为主体，采用哈工大同义词词林和台湾大学 NTUSD 简体中文版本
            进行去重、剔除歧义词汇之后，分别加入正/负面基础情感词典
    2 程度词典: degree_dict
        以中文程度级别词语作为描述情感词的程度词语词典
        How Net 对程度词语进行了级别分类，具体分为 6 个等级: 
            最(most, 0.25) 、很(very, 0.18) 、较(more, 0.15) 、
            稍(-ish, 0.12) 、欠(insufficiently, 0.10) 和超(over, 0.20) 
    3 否定词典: privative_dict 
        词语：'不、没、无、非、莫、弗、勿、毋、未、否、别、無、休、不要、没有、未必、难以、未曾、不能'
        由于否定词在进行情感判断时具有置反作用，所以将其权值设置为－1。
    4 转折归总词典: transitional_dict
        词语：'但、但是、却、然而、不过、只是、就是、总之、总而言之、总体来看、认为、觉得、总结、综上所述'
        文本中可能也会包含对作者观点进行总结的归总类词汇，
            包含这类词汇的分句更能够表达作者的情感倾向，所以需要赋予更高的权重比例

三、其他词典
    1 BosonNLP情感词典：https://bosonnlp.com/dev/resource
        BosonNLP情感词典是从微博、新闻、论坛等数据来源的上百万篇情感标注数据当中自动构建的情感极性词典。
        因为标注包括微博数据，该词典囊括了很多网络用语及非正式简称，对非规范文本也有较高的覆盖率。
        该情感词典可以用于构建社交媒体情感分析引擎，负面内容发现等应用。
        
        在BosonNLP情感词典中，文本采用UTF-8进行编码，每行为一个情感词及其对应的情感分值，
        以空格分隔，共包括114767个词语。其中负数代表偏负面的词语，
        非负数代表偏正面的词语，正负的程度可以由数值的大小反应出。

'''
#%%
import json
from toolkits.setup.specific_func import get_txt_encode


#%% 否定词典
privative_str = '不、没、无、非、莫、弗、勿、毋、未、否、别、無、休、不要、没有、未必、难以、未曾、不能'
privative_wight = -1

privative_dict_list = privative_str.split('、')

file_path = "corpus/sentiment_privative_dict.txt"
f = open(file_path, "w+", encoding='UTF-8')
for line in privative_dict_list:
    f.write(line + ' ' + str(privative_wight) + '\n')
f.close()  

privative_dict = {key:privative_wight for key in privative_str.split('、')}
with open(file_path.replace('txt', 'json'),'w',encoding='utf-8') as json_file:
    json.dump(privative_dict,json_file,ensure_ascii=False)

#%% 转折归总词典
transitional_str = '但、但是、却、然而、不过、只是、就是、总之、总而言之、总体来看、认为、觉得、总结、综上所述'
transitional_wight = 3

transitional_dict_list = transitional_str.split('、')

file_path = "corpus/sentiment_transitional_dict.txt"
f = open(file_path, "w+", encoding='UTF-8')
for line in transitional_dict_list:
    f.write(line + ' ' + str(transitional_wight) + '\n')
f.close()  

transitional_dict = {key:transitional_wight for key in transitional_str.split('、')}
with open(file_path.replace('txt', 'json'),'w',encoding='utf-8') as json_file:
    json.dump(transitional_dict,json_file,ensure_ascii=False)

#%% 程度词典

file_path = "sentiment_dict\HowNet_sentiment\程度级别词语（中文）.txt"
print('********* file_path: ', file_path)

encode = get_txt_encode(file_path)

weight_dict = {'most':0.25,'very':0.18,'more':0.15,
               '-ish':0.12,'insufficiently':0.10,'over':0.20}

degree_dict = {}
degree_dict_list = []
f = open(file_path, 'r', encoding = encode)
weight = 0
weights = 0
for index, line in enumerate(f):
    if index < 2:
        continue
    line = line.replace('\n', '').strip()
    for item in weight_dict:
        if item in line:            
            weights = weight_dict[item]
            print('----  ', line)
            print('----  weights: ', weights)
    if weight != weights:
        weight = weights
        continue
    
    if len(line) > 0:
        print(line, weight)
        degree_dict_list.append([line, weight])
        degree_dict[line] = weight
f.close()

file_path = "corpus/sentiment_degree_dict.txt"
f = open(file_path, "w+", encoding='UTF-8')
for line in degree_dict_list:
    f.write(line[0] + ' ' + str(line[1]) + '\n')
f.close()  

with open(file_path.replace('txt', 'json'),'w',encoding='utf-8') as json_file:
    json.dump(degree_dict,json_file,ensure_ascii=False)
    
#%% 情感词典
file_list = ['正面评价词语（中文）.txt', '正面情感词语（中文）.txt', 
             '负面评价词语（中文）.txt', '负面情感词语（中文）.txt']

emotion_dict = {}
for file_name in file_list:
    if '正' in file_name:
        weight = 1
    else :
        weight = -1
    file_path = "sentiment_dict\HowNet_sentiment\%s"%file_name
    print('********* file_path: ', file_path)
    
    print(file_name, weight)
    encode = get_txt_encode(file_path) 
    
    f = open(file_path, 'r', encoding = encode)
    for index, line in enumerate(f):
        if index < 2:
            continue
        line = line.replace('\n', '').strip()        
        if len(line) > 0:
#            print(line, pos_weight)
            if line in emotion_dict:
                print('-- 已存在：', line)
            else :
#                emotion_dict[line] = weight
                emotion_dict[line] = [weight, file_name]
    f.close()

#%% 同义词
#file_path = "sentiment_dict\synonym.txt"
#encode = get_txt_encode(file_path) 
#f = open(file_path, 'r', encoding = encode)
#
#for index, line in enumerate(f):
#    line_list = line.replace('\n', '').strip().split()        
#    if line_list:
#        for word in line_list:
#            if word in emotion_dict:
#                weight = emotion_dict[word]
#                for word in line_list:
#                    emotion_dict[word] = weight
#                print('-- 已存在：', line)
##            else :
##                emotion_dict[line] = weight
#f.close()

#%% a_level_SP0320.txt
file_path = "sentiment_dict\\a_level_SP0320.txt"
print('********* file_path: ', file_path)

encode = get_txt_encode(file_path) 
f = open(file_path, 'r', encoding = encode)

#emotion_dict = {}

for index, line in enumerate(f):
    line_list = line.replace('\n', '').strip().split() 
    try :       
        if line_list:
            print(line_list)
            word  = line_list[0]
            weight = float(line_list[1].strip())
            if word not in emotion_dict:
#                emotion_dict[word] = weight
                emotion_dict[word] = [weight, file_path]
                print('-- 不存在：', line)
    except Exception as e:
        print(e)
        print(line)
f.close()

#%% neg_words.txt
def update_emotion_dict(emotion_dict, file_path, weight):
    print('********* file_path: ', file_path)
    encode = get_txt_encode(file_path) 
    f = open(file_path, 'r', encoding = encode)
    
    for index, line in enumerate(f):
        line = line.replace('\n', '').strip()
        try :       
            if line not in emotion_dict:
#                emotion_dict[line] = weight
                emotion_dict[line] = [weight, file_path]
                print('-- 不存在：', line)
        except Exception as e:
            print(e)
            print(line)
    f.close()
    
    return emotion_dict

file_path = "sentiment_dict\\neg_words.txt"
emotion_dict = update_emotion_dict(emotion_dict, file_path, weight = -1)

#%% circ
file_path = "sentiment_dict\\circ_neg_self_define.txt"
emotion_dict = update_emotion_dict(emotion_dict, file_path, weight = -1)

file_path = "sentiment_dict\\circ_pos_self_define.txt"
emotion_dict = update_emotion_dict(emotion_dict, file_path, weight = 1)

#%%
emotion_list = []
for key in emotion_dict:
    emotion_list.append([key] + emotion_dict[key])

import pandas as pd
emotion_pd = pd.DataFrame(emotion_list, columns = ['word','weight', 'filename'])

#%%

def decide_label(w):
    if w < 0:
        return -1
    elif w > 0:
        return 1
    elif w == 0:
        return 0
    else :
        print(' -- 出错')
emotion_pd['label'] = emotion_pd['weight'].apply(lambda w: decide_label(w))

emotion_pd.head()
emotion_pd.to_excel("corpus/sentiment_emotion_dict.xlsx", index = False)

#%%
file_path = "corpus/sentiment_emotion_dict.txt"
f = open(file_path, "w+", encoding='UTF-8')
for key,value in emotion_dict.items():
    f.write(key + ' ' + str(value) + '\n')
f.close()  


with open(file_path.replace('txt', 'json'),'w',encoding='utf-8') as json_file:
    json.dump(emotion_dict,json_file,ensure_ascii=False)
#%%

















