#!/usr/bin/python
# -*- coding:utf-8 -*-

from __future__ import division
import re
import jieba
from string import digits
import os
import jieba.posseg as pseg
# from langconv import *
#from toolkits.nlp.langconv import *
#from toolkits.setup.specific_func import Traditional2Simplified

#from nltk.tag import StanfordNERTagger
#chi_tagger = StanfordNERTagger('D:\software\stanford_nlp\chinese.misc.distsim.crf.ser.gz',
#                               'D:\software\stanford_nlp\stanford-ner.jar')

dir_path = os.path.dirname(os.path.abspath(__file__))

stopwords = {}
#stw = open(dir_path + "/corpus/stopwords_20180904.txt", encoding='UTF-8')
stw = open(os.path.normpath(dir_path + r"/corpus/chinese_stopwords.txt"), 
           "r", encoding='UTF-8')
for ws in stw:
    ws = ws.replace("\n", "")
    ws = ws.replace("\r", "")
    stopwords[ws] = 1
stw.close()

from sklearn.base import BaseEstimator, TransformerMixin

class DataFrameSelector(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_names):
        self.attribute_names = attribute_names
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return [d[0] for d in X[:, self.attribute_names]]

class DenseTransformer(TransformerMixin):
    '''spare data to dense data'''
    def transform(self, X, y=None, **fit_params):
        return X.todense()

    def fit_transform(self, X, y=None, **fit_params):
        self.fit(X, y, **fit_params)
        return self.transform(X)

    def fit(self, X, y=None, **fit_params):
        return self
    
#%%
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

def clear_sen(sent):
    '''
    清理句子或正文：
    <font color="#FF0000">  </font>
    <article class="art_box"><h1 class="art_tit_h1">
    </h1><time class="art_time">2018.05.09 12:52:37<cite class="art_cite">
    </cite></time><p class="art_p">
    
    (微信号：wfnews001)
    本文来源：网易湖北                      责任编辑：余蓉_WH07
    电话号码： 95105768   13182876171
    (刘敬元)         关注同花顺财经（ths518），获取更多机会责任编辑：zyk
    (图)  (图片)
    '''
    # \u200b
    sent = sent.replace("\n", "")
    sent = sent.replace('\r','')
    sent = sent.replace('\t','')
    sent = sent.replace('\r\n','')
    sent = sent.replace('\u200b','')
    sent = sent.replace('\xa0','')
    sent = sent.replace("，", ",")
    # sent = sent.replace("。", ".")
    sent = sent.replace("!", "！")
    sent = sent.replace("?", "？")
    sent = sent.replace("(", "（")
    sent = sent.replace(")", "）")

    reobj = re.compile(r"[^\u4e00-\u9fa5。！？“”，：、（）；<>]*")
    sent = reobj.sub("", sent)

    reobj = re.compile('//@(.*?)[:\s]')
    sent = reobj.sub("", sent)
    reobj = re.compile("@(.*?)[:\s]")
    sent = reobj.sub("", sent)
    reobj = re.compile(r"\[[^\[\]]*?\]")
    sent = reobj.sub("", sent)

    # # URL 
    # reobj = re.compile(r'(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?')
    # sent = reobj.sub("", sent)
    # # E-mail
    # reobj = re.compile(r'\w+@([0-9a-zA-Z]+[-0-9a-zA-Z]*)(\.[0-9a-zA-Z]+[-0-9a-zA-Z]*)+')
    # sent = reobj.sub("", sent)
    # # IP
    # reobj = re.compile(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)')
    # sent = reobj.sub("", sent)
    # # 
    # reobj = re.compile(r'<a .*?>(.*?)</a>') 
    # sent = reobj.sub("", sent)    
    # <font color="#FF0000">  </font>
    # reobj = re.compile(r'(?<=<)[/a-zA-Z0-9 ]+=?[“"#a-zA-Z0-9_]*(?=>)')
    # (?# reobj = re.compile(r'(?<=<)[[/a-zA-Z0-9 ]+=?"?[“”#a-zA-Z0-9_]*"?]*(?=>)'))
    # sent = reobj.sub("", sent)
    # （文 徐维建 编辑 孙娟） （专栏作家 聂方义）（记者刘美群）（通讯员 郑浩）
    reobj = re.compile(r'(?<=（)[文|专栏作家|记者|通讯员| |微信号]*[\u4e00-\u9fa5 a-z]{0,}(?=）)')
#    sent = reobj.sub("", sent)
    con_find = reobj.findall(sent)
    if con_find:
        if (sent.find('记者')>0) & (sent.find('记者')<25):
            sent = sent[sent.find('记者')-2:]
    
    sent = reobj.sub("", sent)    
#    reobj = re.compile(r'[责任编辑|更多关于]+[ ：:\u4e00-\u9fa5]*')
#    sent = reobj.sub("", sent)
    # (图)  (图片) (刘敬元)
    reobj = re.compile(r'[(?<=（)|(?<=\()][\u4e00-\u9fa5]{0,3}[(?=）)|(?=))]')
    sent = reobj.sub("", sent)
    # # 身份证号
    # reobj = re.compile(r'([1-9]\d{5}[12]\d{3}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])\d{3}[0-9xX])')
    # sent = reobj.sub("", sent)
    # # 手机号码
    # reobj = re.compile(r'(86)?(1[34578]\d{9})')
    # sent = reobj.sub("", sent)
    # # 固定电话
    # reobj = re.compile(r'\(?(0\d{2,3})?[) -]?\d{7,8}')
    # sent = reobj.sub("", sent)

    return sent

def etl_without_pos(s):  
    # 去除标点和特殊字符
    regex = re.compile(r"[^\u4e00-\u9fa5a-zA-Z0-9]")
    s = regex.sub('', s)

    # 去除字符中的数字
    # remove_digits = str.maketrans('', '', digits)
    # s = s.translate(remove_digits)
    return s

def handle_content(content):
    content = str(content)
    raw = content.strip()
#    raw = Traditional2Simplified(raw) # 繁体字转简体字
    line = ""
    if raw != "":
        # 1 清理字符串
        raw = clear_sen(raw)

        # 2 分词
        # 去掉长度小于3、去掉数字、去掉标点符号
        word_list = filter(lambda x: len(x) > 0, map(etl_without_pos, jieba.cut(raw, cut_all=False)))
        ll = list(word_list)

        # 3 去停用词
        for wd in ll:
        	if wd not in stopwords:
        		line = line + wd.replace(' ', '') + " "
    return line

#def handle_contents(l_contents):
#    # print('。。。 分词 。。。')
#    lines = []
#    for line in l_contents:
#        lines.append(handle_content(line))
#    return lines
#%%
def etl_with_pos(word_pos):  # remove 标点和特殊字符
    regex = re.compile(r"[^\u4e00-\u9fa5a-zA-Z0-9。]")
    word = regex.sub('', word_pos.word)
    
    # 去除字符中的数字
    remove_digits = str.maketrans('', '', digits)
    word = word.translate(remove_digits)    
    word_pos.word = word
    return word_pos

#%% mysql 加载实体词典
def load_entity_dict(dictionarys, pos_flag): 
#    print('更新字典。。。')
    for subject_word in dictionarys:
        jieba.add_word(subject_word, 100, pos_flag)
        jieba.suggest_freq(subject_word, tune = True)
         
def del_entity_dict(dictionarys, pos_flag): 
    for subject_word in dictionarys:
        try :
            jieba.del_word(subject_word)
        except :
            continue
        
def get_pos_word(sentence, pos_flag):
    # 获得词列表
    words_chain = set()
    if sentence == '':
        return words_chain
    else :      
        sentence = sentence.strip()
        words = filter(lambda word_pos: (len(word_pos.word) > 0) and (word_pos.flag == pos_flag), 
                                         map(etl_with_pos, pseg.cut(sentence)))  
        words_chain = set([w.word for w in words])
#        for word, pos in words:        
##            if pos == pos_flag:  # 公司主体     
#                words_chain.add(word)
                
        return words_chain

def get_ner_org(sentence):
    ner_org = set()
    if sentence == '':
        return ner_org
    else :        
        words_pre = handle_content(sentence)
        
        for word, tag in chi_tagger.tag(words_pre.split()):
            if (tag == 'ORGANIZATION') and (len(word) > 3):
                ner_org.add(word)
        return ner_org

def count_value(pos_flag, sentence, count_dict, weight, flag):    
    if flag == 'old':
        sentence_list = get_pos_word(sentence, pos_flag)
    elif flag == 'new':
        sentence_list = get_ner_org(sentence)
        
    if sentence_list:
        for s in sentence_list:
            if s not in count_dict:
                count_dict[s] = sentence.count(s) * weight 
            else :
                count_dict[s] = count_dict[s] + sentence.count(s) * weight 
    return count_dict

def extract_abstract(title, content, dictionarys, pos_flag):
    content = clear_sen(str(content))
    sentences = [i.strip() for i in cut_sentences(content)]
    
    len_thres = 300
    old_content_dict = {}
    if len(content) > len_thres:
        content_1000 = content[:len_thres]
        content_else = content[len_thres:]  
    else :
        content_1000 = content
        content_else = '' 
    
    # ---- 人工标注出的机构： old
    # 计算title中词的值
    old_title_dict = {}
    old_title_dict = count_value(pos_flag, title, old_title_dict,60, 'old')       
    # 计算content中词的值  
    old_content_dict = {}
    old_content_dict = count_value(pos_flag, content_1000, old_content_dict,30, 'old')          
    old_content_dict = count_value(pos_flag, content_else, old_content_dict,10, 'old')       
    # 合并值
    if old_title_dict:
        for key,value in old_title_dict.items():
#                print(key)
            if key not in old_content_dict:
                old_content_dict[key] = old_title_dict[key]
            else :
                old_content_dict[key] = old_content_dict[key] + old_title_dict[key]     
    
    # ---- NER识别出的机构： new
    new_title_dict = {}
    new_content_dict = {}
    if 0:
        # 计算title中词的值                    
        new_title_dict = count_value(title, new_title_dict, 60, 'new')                   
        # 计算content中词的值            
        new_content_dict = count_value(content_1000, new_content_dict,30, 'new')          
        new_content_dict = count_value(content_else, new_content_dict,10, 'new')                     
        # 合并值
        if new_title_dict:
            for key,value in new_title_dict.items():
                if key not in new_content_dict:
                    new_content_dict[key] = new_title_dict[key]
                else :
                    new_content_dict[key] = new_content_dict[key] + new_title_dict[key]   
    
    # 统一名称
    standard_dict = {}
    tmp_dict = {} # 全称 与 subject_word 之间的对应
    if old_content_dict:
        old_content_dict = sorted(old_content_dict.items(), key=lambda x: x[1], reverse=True)
        old_content_dict = {k:v for k,v in old_content_dict}
        for key in old_content_dict:
            if key in dictionarys:
                standard_key = dictionarys[key]
            else :
                standard_key = key
                
            if standard_key not in tmp_dict:
                tmp_dict[standard_key] = [key]
            else :
                tmp_dict[standard_key].append(key)
            
            if standard_key not in standard_dict:                    
                standard_dict[standard_key] = [old_content_dict[key], 'old']
            else :
                standard_dict[standard_key] = [standard_dict[standard_key][0] + old_content_dict[key], 'old']
                
    if new_content_dict:
        new_content_dict = sorted(new_content_dict.items(), key=lambda x: x[1], reverse=True)
        new_content_dict = {k:v for k,v in new_content_dict}            
        for key in new_content_dict:
            if key not in dictionarys:
                standard_key = key
                tmp_dict[standard_key] = [key]              
                standard_dict[standard_key] = [new_content_dict[key], 'new']  
    
    # 获取标题
    for remove_word in ['PP', 'PP平台']:
        if remove_word in standard_dict:
            standard_dict.pop(remove_word)
    
    vip_word = ''
    key_sentence = ''
    org_score_list = []
    purity = 0
    if standard_dict:
        value_list = [value[0] for value in standard_dict.values()]
        purity = int(max(value_list) / sum(value_list) * 100)
        org_score_list = sorted(standard_dict.items(), key=lambda x: x[1][0], reverse=True)              
        if len(org_score_list) > 3:
            org_score_list = org_score_list[:3]
        org_score_list = [[org_s[0]] + org_s[1] for org_s in org_score_list]
        vip_word_list = tmp_dict[org_score_list[0][0]]
#            print('org_score_list: ', org_score_list)
#            print('vip_word_list: ', vip_word_list)
        
        for vip_word in vip_word_list:
            for sentence in sentences:                
                if vip_word in sentence:
                    key_sentence = sentence
                    break
            if key_sentence != '':
                break
        if len(key_sentence) > 100:
            fir_last_len = 30 # 词首尾各20个字符
            if key_sentence != '':
                loc = key_sentence.index(vip_word)
                if loc < fir_last_len:
                    sen_fir = 0
                else :
                    sen_fir = loc - fir_last_len
                if len(key_sentence) - loc < fir_last_len:
                    sen_las = len(key_sentence)
                else :
                    sen_las = loc + fir_last_len + 10
                key_sentence = key_sentence[sen_fir:sen_las]
                    
    return org_score_list, vip_word, key_sentence, purity
#%%
def title_content_label(filepath):
    '''导入预处理后的数据 txt文件'''
    
    filename = filepath + 'titles.txt'
    title = []
    fid = open(filename, "r+", encoding='UTF-8')
    for f in fid:
        title.append(f.strip().replace('\n', ''))
    fid.close()
    print('title num: ', len(title))
    print(title[:2])
    
    content = []
    filename = filepath + 'contents.txt'
    fid = open(filename, "r+", encoding='UTF-8')
    for f in fid:
        content.append(f.strip().replace('\n', ''))
    fid.close()
    print('content num: ', len(content))
    # content[:2]
    
    title_content = [t + ' ' + c for t,c in zip(title, content)]
    print('title_content num: ', len(title_content))
    
    label = []
    filename = filepath + 'labels.txt'
    fid = open(filename, "r+", encoding='UTF-8')
    for f in fid:
        label.append(f.strip().replace('\n', ''))
    fid.close()
    print('label num: ', len(label))
    print(label[:5])
    
    return title_content, label

