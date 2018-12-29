#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import jieba
import jieba.posseg as pseg
import json
import numpy as np
import os
from toolkits.nlp import utils

dir_path = os.path.dirname(os.path.abspath(__file__))
with open(os.path.normpath(dir_path + r"/corpus/all_word_20181221.json"),'r',
          encoding='utf-8') as json_file:
    all_word = json.load(json_file)

sentiment_emotion_dict = {}
for word in all_word['负面词']:
    sentiment_emotion_dict[word] = -1
for word in all_word['正面词']:
    if word not in sentiment_emotion_dict:
        sentiment_emotion_dict[word] = 1
         
with open(os.path.normpath(dir_path + r"/corpus/sentiment_privative_dict.json"),
          'r',encoding='utf-8') as json_file:
    sentiment_privative_dict = json.load(json_file)    
with open(os.path.normpath(dir_path + r"/corpus/sentiment_transitional_dict.json"),
          'r',encoding='utf-8') as json_file:
    sentiment_transitional_dict = json.load(json_file)    
with open(os.path.normpath(dir_path + r"/corpus/sentiment_degree_dict.json"),'r',
          encoding='utf-8') as json_file:
    sentiment_degree_dict = json.load(json_file) 

def load_sentiment_dict():    
    for word in sentiment_emotion_dict:
        jieba.add_word(word, 100, 'emotion')     
    for word in sentiment_privative_dict:        
        jieba.add_word(word, 100, 'privative')    
    for word in sentiment_transitional_dict:
        jieba.add_word(word, 100, 'transitional')    
    for word in sentiment_degree_dict:
        jieba.add_word(word, 100, 'degree')
    return sentiment_emotion_dict, sentiment_privative_dict, sentiment_transitional_dict, sentiment_degree_dict

def del_sentiment_dict():    
    for word in sentiment_emotion_dict:
    	     jieba.del_word(word)     
    for word in sentiment_privative_dict:
    	     jieba.del_word(word)     
    for word in sentiment_transitional_dict:
    	     jieba.del_word(word)     
    for word in sentiment_degree_dict:
    	     jieba.del_word(word) 

def preprocess_sentences(sentences):
    '''
    预处理句子，分词、词性标记
    '''
    pre_sentences = {}
    for sen_loc, sentence in enumerate(sentences):
        pos_list = []
        word_list = []
        
        if sentence.strip() == "":
            pre_sentences[sen_loc] = [pos_list, word_list] # 句子位置、词性、分词结果
            continue
        
        sentence = sentence.strip()
#        words = filter(lambda word_pos: len(word_pos.word) > 0, map(clear_word, pseg.cut(sentence)))
#        print('-- raw: ', sentence)
        sentence = utils.etl_without_pos(sentence)
#        print('-- changed: ', sentence)
        words = pseg.cut(sentence)
        
        for word_pos in words:
#            if word_pos.word not in stopwords: # 去停用词
            pos_list.append(word_pos.flag)
            word_list.append(word_pos.word)
        pre_sentences[sen_loc] = [pos_list, word_list] # 句子位置、词性、分词结果
    return pre_sentences

def decide_sentence(sen_sel):
    '''
    判断句子是否符合排除规则。
    如果符合，即便该句含有实体，也跳过。
    '''
    reobj = re.compile(r'([0-9]\d{5})')
    sent_1 = reobj.findall(sen_sel)   
    reobj = re.compile(r'(20\d{2}[-|年| ]\d{2}[-|月| ]\d{2}[-|日| ][ ]*\d{2}[:|：| ]\d{2}[:|：| ]*\d{0,2}[:|：| ]*)')
    sent_2 = reobj.findall(sen_sel)    

    if len(str(sen_sel)) > 800: # 句子长度大于1000
        return -1
    elif len(sent_1) > 2: # 识别六位股票代码
        return -2    
    elif len(sent_2) > 0: # 识别六位股票代码
        return -3
    elif sen_sel.count(' ') > 10: # 空格个数多余10
        return -4
    else:
        return 1
                
def get_entity(pre_sentences, sentences, dictionarys):
    '''
    获取实体
    '''    
    org_list = []
    repeat_id = set()
    org_loc = {}
    
    for sen_loc, [pos_list, word_list] in pre_sentences.items():
        sen_sel = sentences[sen_loc]
        decide_sen = decide_sentence(sen_sel)
        
        if decide_sen < 0: # 句子排除规则
            print('decide_sen: ', decide_sen)
            continue
        else :                    
            cpns = []
            aka_names = []
            for pos, word in zip(pos_list, word_list):
                if pos == 'cpn':  # 公司主体
                    try:
                        cpns.append(dictionarys[word])  # (id, classify_id, node_id, org_name)
                        aka_names.append(word)
                        if word not in org_loc:
                            org_loc[word] = [dictionarys[word][3], {sen_loc}]
                        else :
                            org_loc[word][1].add(sen_loc) 
                    except:
                        continue  
                          
            if len(cpns) > 0: 
                for cpn, aka_name in zip(cpns, aka_names):
                    if cpn[2] not in repeat_id:                            
                        dict_ = {"id": cpn[0], "classify_id": cpn[1], "node_id": cpn[2], 
                                 "name": cpn[3], "aka_name": aka_name}
                        org_list.append(dict_)
                        repeat_id.add(cpn[2])
    return org_list, org_loc                    

def get_range(seed, num_range, num_min, num_max, step = 1):   
    '''
    获取种子点（seed）左右各 n 个（num_range）数字
    '''         
#    seed = 12
#    step = 1
#    num_range = 1 # 左右各3个
#    num_max = 12
#    num_min = 0
    
    range_list = []
    for i in range(seed - num_range, seed + num_range + 1, step):
        if i >= num_min and i <= num_max:
            range_list.append(i)
    return range_list

#%%
def cal_sen_tend(sen_loc, pre_sentence):
    '''
    计算一句的倾向性
    '''
    tendence_score = 0
    
    pos_list = pre_sentence[0]
    word_list = pre_sentence[1]
    word_weight = []
    for pos, word in zip(pos_list, word_list):    
        if pos == 'emotion':
            word_weight.append(sentiment_emotion_dict[word])
        elif pos == 'degree':
            word_weight.append(sentiment_degree_dict[word])            
        else :
            word_weight.append(0)
    
    rule_index = 0
    if 'emotion' in pos_list:
       # 只有 情感词 ，规则1  
       rule_index = 1
       tendence_score = 0
       for loc, pos in enumerate(pos_list):
           if pos == 'emotion':
               tendence_score = tendence_score + word_weight[loc]
       if sen_loc < 3:
           tendence_score = tendence_score * 3
       
       if ('privative' in pos_list) and ('degree' not in pos_list):
           # 情感词、否定词 ，规则2
           # 情感词汇之前 5 个词汇中的否定词个数
            rule_index = 2
            tendence_score = 0
            for loc, pos in enumerate(pos_list):
                if pos == 'emotion':
                    if loc > 5:
                        test_loc = loc - 5
                    else :
                        test_loc = 5 - loc
                    test_list = pos_list[test_loc:loc]
                    if 'privative' in test_list:
                        tendence_score += word_weight[loc] * (-1) ** test_list.count('privative')
                    else :
                        tendence_score += word_weight[loc]                        
           
       elif ('privative' not in pos_list) and ('degree' in pos_list):
           # 情感词、程度词 ，规则3
           # 情感词汇前后各 3 个
            rule_index = 3
            tendence_score = 0
            for loc, pos in enumerate(pos_list):
                if pos == 'emotion':
                    pos_test_index =  get_range(loc, 3, 0, len(pos_list)-1 , step = 1)            
                    test_list = pos_list[min(pos_test_index):max(pos_test_index)]
                    test_weight = word_weight[min(pos_test_index):max(pos_test_index)]
                    if 'degree' in test_list:
                        tendence_score += word_weight[loc] * test_weight[test_list.index('degree')]
                    else :
                        tendence_score += word_weight[loc]           
       elif ('privative' in pos_list) and ('degree' in pos_list):
           # 情感词、否定词、程度词 ，规则4/5
           tendence_score = 0
           if pos_list.index('degree') < pos_list.index('privative'):
               # 否定词位于程度词之前, 否定词和程度词的位置信息权重: 0.8
               rule_index = 4
               weight = 0.5
           elif pos_list.index('degree') > pos_list.index('privative'):
               # 否定词位于程度词之后, 否定词和程度词的位置信息权重: 1.2
               rule_index = 5
               weight = 1.5
               
           for loc, pos in enumerate(pos_list):
               if pos == 'emotion':
#                   print(' ---- ', loc)
                   if loc > 5:
                       test_loc = loc - 5
                   else :
                       test_loc = 5 - loc
                   test_list_privative = pos_list[test_loc:loc]                    
                
                   pos_test_index =  get_range(loc, 3, 0, len(pos_list) , step = 1)            
                   test_list_degree = pos_list[min(pos_test_index):max(pos_test_index)]
                   test_weight = word_weight[min(pos_test_index):max(pos_test_index)]
                   
                   if ('privative' in test_list_privative) and ('degree' not in test_list_degree):
                       tendence_score += word_weight[loc] * (-1) ** test_list_privative.count('privative')
                   elif ('privative' not in test_list_privative) and ('degree' in test_list_degree):
                       tendence_score += word_weight[loc] * test_weight[test_list_degree.index('degree')]
                   elif ('privative' in test_list_privative) and ('degree' in test_list_degree):
                       tendence_score += weight * word_weight[loc] * test_weight[test_list_degree.index('degree')] * (-1) ** test_list_privative.count('privative')                   
                   else :
                       tendence_score += word_weight[loc]   
#                   print(tendence_score)

       if 'transitional' in pos_list:
           # 包含 转折归总词 ，规则6
           rule_index = 6
           tendence_score = 1.5 * tendence_score
    return tendence_score, rule_index

def cal_sentences_tendency(pre_sentences, org_loc, sentences):
    '''
    计算实体所在句及前后各一句所在的情感倾向
    '''
    sen_loc_max = max(pre_sentences.keys())
    sen_loc_min = min(pre_sentences.keys())
    num_range = 0 # 1 左右各一个数字，共三个
    org_score_dict = {}
    org_sen_loc = {}
    org_sentences_pos_word_weight = {}
    
    for org in org_loc:
        name = org_loc[org][0]
        sen_loc_list = org_loc[org][1]        
        org_score_list = []
        sentences_pos_word_weight = []
        for sen_loc in sen_loc_list:       
            # 获取 左中右共三句话，计算倾向值，并取平均值
            sentence_index_list =  get_range(sen_loc, num_range, 
                                        sen_loc_min, sen_loc_max, step = 1)
            
            for sen_index in sentence_index_list:
                pre_sentence = pre_sentences[sen_index]
                tendence_score, rule_index = cal_sen_tend(sen_index, pre_sentence)
                org_score_list.append(tendence_score)
                pos_word_weight = []                
                for pos,word in zip(pre_sentence[0], pre_sentence[1]):
                    if pos in ['emotion', 'privative', 'transitional', 'degree']:
                        if pos == 'emotion':
                            weight = sentiment_emotion_dict[word]
                        elif pos == 'degree':
                            weight = sentiment_degree_dict[word] 
                        elif pos == 'privative':
                            weight = 0.8 
                        elif pos == 'transitional':
                            weight = 1.2                              
                        pos_word_weight.append((pos, word, weight)) 
                sentences_pos_word_weight.append([sen_loc, sen_index, 
                                                  tendence_score, rule_index,
                                                  sentences[sen_index], 
                                                  pos_word_weight])
        
        if name not in org_sentences_pos_word_weight:
            org_sentences_pos_word_weight[name] = sentences_pos_word_weight
        else :
            org_sentences_pos_word_weight[name] += sentences_pos_word_weight
        
        if name not in org_score_dict:
            org_score_dict[name] = [np.mean(org_score_list)]
            org_sen_loc[name] = [sentence_index_list]
        else :
            org_score_dict[name].append(np.mean(org_score_list))
            org_sen_loc[name].append(sentence_index_list)
    
    # 一个主体多次出现，取平均值
    for key in org_score_dict:
        org_score_dict[key] = np.mean(org_score_dict[key])
            
    return org_score_dict, org_sen_loc, org_sentences_pos_word_weight

#%%
def get_entity_new(pre_sentences, sentences, dictionarys):
    '''
    获取实体
    '''    
    org_list = []
    repeat_id = set()
    org_loc = {}
    sentence_flag = 0
    aka_name_id = {}
    aka_name_dict = {}
    for sen_loc, [pos_list, word_list] in pre_sentences.items():  
        sen_sel = sentences[sen_loc]
        decide_sen = decide_sentence(sen_sel)

        if decide_sen < 0: # 句子排除规则
            print('decide_sen: ', decide_sen)
            continue
        else :          
            cpns = []
            aka_names = []            
            if ('rm' not in pos_list) & ('cpn' in pos_list):   # 含 去除词 的句子需过滤掉   
                for pos, word in zip(pos_list, word_list):                
                    if pos == 'cpn':  # 公司主体   
                        try :
                            word_id_list = dictionarys['subject_word_list'][word]  # 一个主体词对应多个id  
    #                        print(word, word_id_list)
                            for word_id in word_id_list:
    #                            print(word_id, '--')
                                if dictionarys['data'][word_id][5] != '':  
                                    # 辅助词A不为空
                                    for worda in word_list:
                                        assista_word_list = dictionarys['data'][word_id][5].split(' ')
    #                                    if '保险' in assista_word_list: assista_word_list.remove('保险')  
                                        if worda in assista_word_list: # 该句中含辅助词A
                                            if dictionarys['data'][word_id][6] != '':    
                                                # 辅助词B不为空
                                                for wordb in word_list:
                                                    if wordb in dictionarys['data'][word_id][6].split(' '):# 该句中含辅助词B
                                                        sentence_flag = 1
    #                                                    print(word_id, wordb, 'C')
                                            else :
                                                sentence_flag = 1
    #                                            print(word_id,worda, 'B')                                                  
                                else :
                                    sentence_flag = 1
    #                                print(word_id,'A')    
                                    
                                if sentence_flag:                                  
                                    cpns.append(dictionarys['data'][word_id])
                                    aka_names.append(word)
                                    aka_name_id[word_id] = word
                                    aka_name_dict[word] = [dictionarys['data'][word_id][3], 
                                                  dictionarys['data'][word_id][1]]## name, classify_id
                                    if word_id not in org_loc:
                                        org_loc[word_id] = [dictionarys['data'][word_id][3],
                                                         {sen_loc}]                                     
                                    else :
                                        org_loc[word_id][1].add(sen_loc) 
                                    sentence_flag = 0
                        except :
                            continue 
                              
        if len(cpns) > 0: # 符合一个主体词、两个辅助词、一个去除词的规则
            for cpn, aka_name in zip(cpns, aka_names):
                if cpn[2] not in repeat_id:                            
                    dict_ = {"id": cpn[0], "classify_id": cpn[1], "node_id": cpn[2], 
                             "name": cpn[3], "aka_name": aka_name}
                    org_list.append(dict_)
                    repeat_id.add(cpn[2])
                    
    org_locs = [[aka_name_id[k],v] for k,v in org_loc.items()]
    return org_list, org_locs, aka_name_dict                  

def cal_sentences_tendency_new(pre_sentences, org_loc, sentences):
    '''
    计算实体所在句及前后各一句所在的情感倾向
    '''
    sen_loc_max = max(pre_sentences.keys())
    sen_loc_min = min(pre_sentences.keys())
    num_range = 1 # 左右各一个数字，共三个
    org_score_dict = {}
    org_sen_loc = {}
    org_sentences_pos_word_weight = {}
    
#    for org in org_loc:
#        name = org_loc[org][0]
#        sen_loc_list = org_loc[org][1]   
        
    for [org, value] in org_loc:
        name = value[0]
        sen_loc_list = value[1]           
        org_score_list = []
        sentences_pos_word_weight = []
        for sen_loc in sen_loc_list:       
            # 获取 左中右共三句话，计算倾向值，并取平均值
            sentence_index_list =  get_range(sen_loc, num_range, 
                                        sen_loc_min, sen_loc_max, step = 1)
            
            for sen_index in sentence_index_list:
                pre_sentence = pre_sentences[sen_index]
                tendence_score, rule_index = cal_sen_tend(sen_index, pre_sentence)
                org_score_list.append(tendence_score)
                pos_word_weight = []                
                for pos,word in zip(pre_sentence[0], pre_sentence[1]):
                    if pos in ['emotion', 'privative', 'transitional', 'degree']:
                        if pos == 'emotion':
                            weight = sentiment_emotion_dict[word]
                        elif pos == 'degree':
                            weight = sentiment_degree_dict[word] 
                        elif pos == 'privative':
                            weight = 0.8 
                        elif pos == 'transitional':
                            weight = 1.2                              
                        pos_word_weight.append((pos, word, weight)) 
                sentences_pos_word_weight.append([sen_loc, sen_index, 
                                                  tendence_score, rule_index,
                                                  sentences[sen_index], 
                                                  pos_word_weight])
        
        if name not in org_sentences_pos_word_weight:
            org_sentences_pos_word_weight[name] = sentences_pos_word_weight
        else :
            org_sentences_pos_word_weight[name] += sentences_pos_word_weight
        
        if name not in org_score_dict:
            org_score_dict[name] = [np.mean(org_score_list)]
            org_sen_loc[name] = [sentence_index_list]
        else :
            org_score_dict[name].append(np.mean(org_score_list))
            org_sen_loc[name].append(sentence_index_list)
    
    # 一个主体多次出现，取平均值
    for key in org_score_dict:
        org_score_dict[key] = np.mean(org_score_dict[key])
            
    return org_score_dict, org_sen_loc, org_sentences_pos_word_weight
#%%