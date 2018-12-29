#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import jieba
import jieba.posseg as pseg
from string import digits
import json
import numpy as np
import os
dir_path = os.path.dirname(os.path.abspath(__file__))


# 加载自定义词典
jieba.load_userdict(dir_path + '/corpus/insurance_dict_20180803.txt')
             
stopwords = {}
stw = open(dir_path + "/corpus/stopwords_20180904.txt", encoding='UTF-8')
for ws in stw:
    ws = ws.replace("\n", "")
    ws = ws.replace("\r", "")
    stopwords[ws] = 1
stw.close()

#%%
from toolkits.nlp import circ_dict_dbutils

# mysql 加载实体词典
dictionarys = circ_dict_dbutils.get_dicts()
for dictionary in dictionarys:
    jieba.add_word(dictionary, 100, "cpn")

#%%
def clear_article(content):
    content = content.replace("\n", "")
    content = content.replace('\r', '')
    content = content.replace('\r\n', '')
    return content

def clear_word(sentence):  # remove 标点和特殊字符,英文字母
    regex = re.compile(r"[^\u4e00-\u9fa5，、；：]")
    word = regex.sub('', sentence)
    
    # 去除字符中的数字
    remove_digits = str.maketrans('', '', digits)
    word = word.translate(remove_digits)    
    return word

#def cut_sentences(sentence):
#    '''
#    中文，依据标点符号分句：。！？
#    '''
#    puns = frozenset(u'。！？')
#    tmp = []
#    for ch in sentence:
#        tmp.append(ch)
#        if puns.__contains__(ch):
#            yield ''.join(tmp)
#            tmp = []
#    yield ''.join(tmp)


def cut_sentences(para):
    para = re.sub('([。！？\?])([^”])',r"\1\n\2",para) # 单字符断句符
    para = re.sub('(\.{6})([^”])',r"\1\n\2",para) # 英文省略号
    para = re.sub('(\…{2})([^”])',r"\1\n\2",para) # 中文省略号
    para = re.sub('(”)','”\n',para)   # 把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    para = para.rstrip()       # 段尾如果有多余的\n就去掉它
    #很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    return para.split("\n")

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
        sentence = clear_word(sentence)
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
                
def get_entity(pre_sentences, sentences, dictionarys = dictionarys):
    '''
    获取实体 保监会旧平台
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

#%%














