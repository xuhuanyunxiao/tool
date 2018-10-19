#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import jieba
import jieba.posseg as pseg
from string import digits
import json
import numpy as np

# 加载自定义词典
jieba.load_userdict('corpus/insurance_dict_20180803.txt')

org_company_list = set()
f = open('circ_sel_org_and_company.txt', 'r', encoding = 'utf-8-sig')
for line in f.readlines():
    org_company_list.add(line.strip())
f.close()
#%%
with open("corpus/sentiment_emotion_dict.json",'r',encoding='utf-8') as json_file:
    sentiment_emotion_dict = json.load(json_file)             
with open("corpus/sentiment_privative_dict.json",'r',encoding='utf-8') as json_file:
    sentiment_privative_dict = json.load(json_file)    
with open("corpus/sentiment_transitional_dict.json",'r',encoding='utf-8') as json_file:
    sentiment_transitional_dict = json.load(json_file)    
with open("corpus/sentiment_degree_dict.json",'r',encoding='utf-8') as json_file:
    sentiment_degree_dict = json.load(json_file)    
    
def load_sentiment_dict():    
    for word in sentiment_emotion_dict:
        jieba.add_word(word, 10, 'emotion')     
    for word in sentiment_privative_dict:        
        jieba.add_word(word, 10, 'privative')    
    for word in sentiment_transitional_dict:
        jieba.add_word(word, 10, 'transitional')    
    for word in sentiment_degree_dict:
        jieba.add_word(word, 10, 'degree')

load_sentiment_dict()

def del_sentiment_dict():    
    for word in sentiment_emotion_dict:
    	     jieba.del_word(word)     
    for word in sentiment_privative_dict:
    	     jieba.del_word(word)     
    for word in sentiment_transitional_dict:
    	     jieba.del_word(word)     
    for word in sentiment_degree_dict:
    	     jieba.del_word(word)     

#del_sentiment_dict()

#%%
# mysql 加载实体词典
def load_mysql_dict(dictionarys): 
    for subject_word in dictionarys['subject_word_list']:
	     jieba.add_word(subject_word, 100, "cpn")
    for assist_worda in dictionarys['assistA_word_list']:
	     jieba.add_word(assist_worda, 100, "assist_a")
    for assist_wordb in dictionarys['assistB_word_list']:
	     jieba.add_word(assist_wordb, 100, "assist_b")
    for remove_word in dictionarys['remove_word_list']:
	     jieba.add_word(remove_word, 100, "rm")

def del_mysql_dict(dictionarys): 
    for subject_word in dictionarys['subject_word_list']:
        try :
            jieba.del_word(subject_word)
        except :
            continue
    for assist_worda in dictionarys['assistA_word_list']:
        try :        
            jieba.del_word(assist_worda)
        except :
            continue            
    for assist_wordb in dictionarys['assistB_word_list']:
        try :        
    	     jieba.add_word(assist_wordb)
        except :
            continue             
    for remove_word in dictionarys['remove_word_list']:
        try :        
    	     jieba.del_word(remove_word)       
        except :
            continue     

#%%
def clear_article(content):
    content = content.replace("\n", "")
    content = content.replace('\r', '')
    content = content.replace('\r\n', '')
    return content

def clear_word(word_pos):  # remove 标点和特殊字符
    regex = re.compile(r"[^\u4e00-\u9f5aa-zA-Z0-9。]")
    word = regex.sub('', word_pos.word)
    
    # 去除字符中的数字
    remove_digits = str.maketrans('', '', digits)
    word = word.translate(remove_digits)    
    word_pos.word = word
    return word_pos

def cut_sentences(sentence):
    '''
    中文，依据标点符号分句：。！？
    '''
    puns = frozenset(u'。！？')
    tmp = []
    for ch in sentence:
        tmp.append(ch)
        if puns.__contains__(ch):
            yield ''.join(tmp)
            tmp = []
    yield ''.join(tmp)

def preprocess_sentences(sentences):
    '''
    预处理句子，分词、词性标记
    '''
    pre_sentences = {}
    for sen_loc, sentence in enumerate(sentences):
        if sentence.strip() == "":
            continue
        
        sentence = sentence.strip()
        words = filter(lambda word_pos: len(word_pos.word) > 0, map(clear_word, pseg.cut(sentence)))
        
        pos_list = []
        word_list = []
        for word_pos in words:
            pos_list.append(word_pos.flag)
            word_list.append(word_pos.word)
        pre_sentences[sen_loc] = [pos_list, word_list] # 句子位置、词性、分词结果
    return pre_sentences
    
def get_entity(pre_sentences, dictionarys):
    '''
    获取实体
    '''    
    org_list = []
    repeat_id = set()
    org_loc = {}
    for sen_loc, [pos_list, word_list] in pre_sentences.items():            
        sentence_flag = 0
        cpns = []
        if ('rm' not in pos_list) & ('cpn' in pos_list):   # 含 去除词 的句子需过滤掉   
            for pos, word in zip(pos_list, word_list):
                if pos == 'cpn':  # 公司主体   
                    try :
                        word_id_list = dictionarys['subject_word_list'][word]  # 一个主体词对应多个id  
                        for word_id in word_id_list:
                            if dictionarys['data'][word_id][5] != '':  # 辅助词A不为空
                                for worda in word_list:
                                    if worda in dictionarys['data'][word_id][5].split(' '): # 该句中含辅助词A
                                        if dictionarys['data'][word_id][6] != '':    # 辅助词B不为空
                                            for worda in word_list:
                                                if worda in dictionarys['data'][word_id][6].split(' '):# 该句中含辅助词B
                                                    sentence_flag = 1
                                        else :
                                            sentence_flag = 1
                            else :
                                sentence_flag = 1
                            
                            if sentence_flag:
                                if dictionarys['data'][word_id][3] in org_company_list:                                    
                                    cpns.append(dictionarys['data'][word_id])
                                    if word not in org_loc:
                                        org_loc[word] = [dictionarys['data'][word_id][3],
                                                         {sen_loc}]
                                    else :
                                        org_loc[word][1].add(sen_loc) 
                    except :
                        continue 
                      
        if len(cpns) > 0: # 符合一个主体词、两个辅助词、一个去除词的规则
            for cpn in cpns:
                if cpn[2] not in repeat_id:                            
                    dict_ = {"id": cpn[0], "classify_id": cpn[1], "node_id": cpn[2], 
                             "name": cpn[3]}
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
       if sen_loc < 3:
           tendence_score = sum(word_weight) * 3
       else :
           tendence_score = sum(word_weight)
       
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
               weight = 0.8
           elif pos_list.index('degree') > pos_list.index('privative'):
               # 否定词位于程度词之后, 否定词和程度词的位置信息权重: 1.2
               rule_index = 5
               weight = 1.2
               
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
           tendence_score = 1.2 * tendence_score
    return tendence_score, rule_index

def cal_sentences_tendency(pre_sentences, org_loc, sentences):
    '''
    计算实体所在句及前后各一句所在的情感倾向
    '''
    sen_loc_max = max(pre_sentences.keys())
    sen_loc_min = min(pre_sentences.keys())
    num_range = 1 # 左右各一个数字，共三个
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
                        pos_word_weight.append((pos, word, weight)) 
                sentences_pos_word_weight.append([sen_loc, sen_index, 
                                                  tendence_score, rule_index,
                                                  sentences[sen_index], 
                                                  pos_word_weight])
        
        if name not in org_sentences_pos_word_weight:
            org_sentences_pos_word_weight[name] = sentences_pos_word_weight
        else :
            org_sentences_pos_word_weight[name].append(sentences_pos_word_weight)
        
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
def evaluate_article(title, content, dictionarys):
    '''
    计算一篇文章倾向、以及每个主体的倾向
    '''
    
    load_mysql_dict(dictionarys)
    # title
    pre_titles = preprocess_sentences([title])
    pre_title = pre_titles[0]
    title_score, title_rule_index = cal_sen_tend(0, pre_title)
    
    title_pos_word = []
    for pos,word in zip(pre_title[0], pre_title[1]):
        if pos in ['emotion', 'privative', 'transitional', 'degree']:
            if pos == 'emotion':
                weight = sentiment_emotion_dict[word]
            elif pos == 'degree':
                weight = sentiment_degree_dict[word]  
            title_pos_word.append((pos, word, weight))
    
    # content
    content = clear_article(str(content))  # clear_article
    sentences = [i.strip() for i in cut_sentences(content)]
    pre_sentences = preprocess_sentences(sentences)
    org_list, org_loc = get_entity(pre_sentences, dictionarys)
    org_score_dict, org_sen_loc, org_sentences_pos_word_weight = cal_sentences_tendency(pre_sentences, 
                                                                                        org_loc, sentences)
    
    org_score_list = []
    for cpn in org_list:
        cpn['org_tendency_score'] = org_score_dict[cpn['name']]
        org_score_list.append(cpn)
        
    # 计算篇章倾向
    content_score = 0
    if org_score_list:
        for org_score in org_score_list:
            content_score += org_score['org_tendency_score']

    chapter_tendency_score = title_score * 0.6 + content_score * 0.4

    del_mysql_dict(dictionarys)

    return chapter_tendency_score, org_score_list, title_score, content_score, title_rule_index, title_pos_word, org_sentences_pos_word_weight

def process_articles(titles, contents, dictionarys):
    org_res = []
    chapter_res = []
    for title, content in zip(titles, contents):
        chapter_tendency_score, org_score_list = evaluate_article(title, content, dictionarys)
        chapter_res.append(chapter_tendency_score)
        org_res.append(org_score_list)
    return chapter_res, org_res

#%%
if __name__ == '__main__':
    import json
    import dict_dbutils  
    
    dictionarys_2 = dict_dbutils.get_dicts(types = '1') # 保监会    
    dictionarys = dictionarys_2
    
    import pandas as pd

#    data = pd.read_excel('Q3数据带ID.xlsx')
#    data = pd.read_excel('circ_class_predict_mysql_2018-10-07.xlsx')
#    data = data.iloc[:30, :]
    titles = data['title'].tolist()
    contents = data['content'].tolist()
#%%    
    org_res = []
    chapter_res = []
    index = -1
    for title, content in zip(titles, contents):
        try :
            index += 1
            
            id = data.loc[index, 'id']
            predict_label = data.loc[index, 'predict_label']
            chapter_tendency_score, org_score_list, title_score, \
            content_score, title_rule_index, title_pos_word, \
            org_sentences_pos_word_weight = evaluate_article(title, content, dictionarys)
            chapter_res.append([id, predict_label, title,content, 
                                chapter_tendency_score, title_score, 
                                content_score, title_rule_index, 
                                str(title_pos_word), str(org_score_list), 
                                str(org_sentences_pos_word_weight)])
            org_res.append(org_score_list)
            
        except Exception as e:
            print(index)
            print(e)
            continue
        
    ss = 'id,predict_label,title,content,chapter_tendency_score,\
            title_score,content_score,title_rule_index,\
            title_pos_word,org_score_list,org_sentences_pos_word_weight'
    chapter_res = pd.DataFrame(chapter_res, columns = ss.split(','))
    chapter_res.to_excel('circ_chapter_tendency_score_300.xlsx', index = False)   
#%%   
    