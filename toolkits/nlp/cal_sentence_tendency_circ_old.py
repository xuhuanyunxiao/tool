#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jieba
from toolkits.nlp import utils
from toolkits.nlp import utils_tendency
import os

dir_path = os.path.dirname(os.path.abspath(__file__))
# 加载自定义词典
jieba.load_userdict(os.path.normpath(dir_path + r"/corpus/insurance_dict_20180803.txt"))

sentiment_emotion_dict, sentiment_privative_dict, \
    sentiment_transitional_dict, sentiment_degree_dict = utils_tendency.load_sentiment_dict()
# utils_tendency.del_sentiment_dict()

#%%
import dict_dbutils

# mysql 加载实体词典
dictionarys = dict_dbutils.get_dicts()
for dictionary in dictionarys:
    jieba.add_word(dictionary, 100, "cpn")

def evaluate_article(title, content, dictionarys):
    '''
    计算一篇文章倾向、以及每个主体的倾向
    '''
    
#    load_mysql_dict(dictionarys)
    # title
    pre_titles = utils_tendency.preprocess_sentences([title])
    pre_title = pre_titles[0]
    title_score, title_rule_index = utils_tendency.cal_sen_tend(0, pre_title)
    
    title_pos_word = []
    for pos,word in zip(pre_title[0], pre_title[1]):
        if pos in ['emotion', 'privative', 'transitional', 'degree']:
            if pos == 'emotion':
                weight = sentiment_emotion_dict[word]
            elif pos == 'degree':
                weight = sentiment_degree_dict[word]  
            elif pos == 'privative':
                weight = 0.8 
            elif pos == 'transitional':
                weight = 1.2                  
            title_pos_word.append((pos, word, weight))
    
    pre_title = [[p,w] for p,w in zip(pre_title[0], pre_title[1])]
    
    # content
    content = utils.clear_sen(str(content))  # clear_article
    sentences = [i.strip() for i in utils.cut_sentences(content)]
    pre_sentences = utils_tendency.preprocess_sentences(sentences)    
    
    content_score = 0
    org_score_list = []
    org_sentences_pos_word_weight = []
    if len(pre_sentences) > 0:
        org_list, org_loc = utils_tendency.get_entity(pre_sentences, sentences, dictionarys = dictionarys)                    
        org_score_dict, org_sen_loc, \
        org_sentences_pos_word_weight = utils_tendency.cal_sentences_tendency(pre_sentences, 
                                                               org_loc, sentences)    

        for cpn in org_list:
            # 选出 保险机构 用于判断倾向性 （classify_id = 40
            if cpn['classify_id'] in [9,]:
                try :
                    cpn['org_tendency_score'] = org_score_dict[cpn['name']]
                except:
                    cpn['org_tendency_score'] = org_score_dict[cpn['aka_name']]
                    
                content_score += cpn['org_tendency_score']
                
            else :
                cpn['org_tendency_score'] = 0 # 未选择的机构都为非负 
                
            # 转换成两类
            if cpn['org_tendency_score'] < 0:
                cpn['org_tendency_score'] = -1
            else:
                cpn['org_tendency_score'] = 0                
                
            org_score_list.append(cpn)     

    pre_sentences = [[p,w] for p,w in zip(pre_sentences[0][0], pre_sentences[0][1])]
    chapter_tendency_score = title_score * 0.6 + content_score * 0.4

    # 转换成两类
    if chapter_tendency_score < 0:
        chapter_tendency_score = -1
    else:
        chapter_tendency_score = 0

#    del_mysql_dict(dictionarys)
    return chapter_tendency_score, org_score_list
#    return chapter_tendency_score, org_score_list, title_score, content_score, title_rule_index, title_pos_word, org_sentences_pos_word_weight

def process_articles(titles, contents): # , dictionarys
    org_res = []
    chapter_res = []
    for title, content in zip(titles, contents):
        chapter_tendency_score, org_score_list = evaluate_article(title, content, dictionarys)
        chapter_res.append(chapter_tendency_score)
        org_res.append(org_score_list)
    return chapter_res, org_res

def write_txt(filename, index, ID, org, flag):
#    print(filename, index, ID, org, flag)
    
    file = open(r'D:\XH\Python_Project\proj_3_wzty\circ\Q3_data\circ_tend_scores.txt', 
                'a', encoding = 'utf-8')
    file.write('{0}, {1}, {2}, {3}, {4} \n'.format(filename, index, ID, org, flag))
    file.close()    

#%%
def print_res(y_test, y_pred_class):
#    y_pred_class = data['倾向'].tolist()
#    y_test = data['误判'].tolist()
    print('accuracy_score: ', metrics.accuracy_score(y_test, y_pred_class)) # 指所有分类正确的百分比
    print(metrics.classification_report(y_test, y_pred_class))
    print('confusion_matrix: ')
    print( metrics.confusion_matrix(y_test, y_pred_class))
    
#%%
if __name__ == '__main__':
    import pandas as pd
    from sklearn import metrics
    from collections import Counter
    data = pd.read_excel('circ_sentences_tendency_20181224(1208-1210).xlsx') # , sheet_name = 'data'
    data['index'] = range(data.shape[0])
#    data = data.loc[:1000, :]
#    print_res(data['误判'].tolist(), data['倾向'].tolist())
#    print_res(data['误判'].tolist(), data['新-倾向'].tolist())
#%%    
    predict_label = []
    sentence_res = []
    print('data: ', data.shape)
    for index in data.index:
#        label_1 = data.loc[index, '误判']
#        label_0 = data.loc[index, '倾向']
#        label_2 = data.loc[index, '新-倾向']
        title = data.loc[index, 'sentence']
        
        pre_titles = utils_tendency.preprocess_sentences([str(title)])
        pre_title = pre_titles[0]
        title_score, title_rule_index = cal_sen_tend(0, pre_title)
        if title_score < 0:
            label_3 = -1
        elif title_score > 0:
            label_3 = 1
        else :
            label_3 = 0
        predict_label.append(label_3)
            
        title_pos_word = []
        for pos,word in zip(pre_title[0], pre_title[1]):
            if pos in ['emotion', 'privative', 'transitional', 'degree']:
                if pos == 'emotion':
                    weight = sentiment_emotion_dict[word]
                elif pos == 'degree':
                    weight = sentiment_degree_dict[word]  
                elif pos == 'privative':
                    weight = 0.8 
                elif pos == 'transitional':
                    weight = 1.2                  
                title_pos_word.append((pos, word, weight))     
                
        sentence_res.append([index, label_3, title, title_score, str(pre_title),  
                             title_rule_index, str(title_pos_word)]) # label_2,
                
#    print_res(data['误判'].tolist(), predict_label)
    sentence_res = pd.DataFrame(sentence_res, columns = ['index', 'predict_label', 
                                                         'pre_sentence','score', 'pre_title', 
                                                         'rule_index', 'title_pos_word']) # '新-新-倾向', 
    print('sentence_res: ', sentence_res.shape)
    data_res = pd.merge(data, sentence_res, on='index')
    print('data_res: ', data_res.shape)
    data_res.to_excel('circ_sentences_tendency_predict_20181224(1208-1210).xlsx', index = False)
 