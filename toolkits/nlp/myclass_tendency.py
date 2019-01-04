#!/usr/bin/python
# -*- coding:utf-8 -*-
#%%
from sklearn.base import BaseEstimator, TransformerMixin
import random
import numpy as np
import os
import json
    
#%%        
class StatsFeatures_tendency(BaseEstimator, TransformerMixin):
    
    def __init__(self):
        self.corpus_path = os.path.dirname(os.path.abspath(__file__))
        print(self.corpus_path)
        
#        self.neg = set()
#        f = open(os.path.normpath(self.corpus_path + "/corpus/neg_words.txt"),
#                 "r+", encoding='UTF-8')
#        for content in f:
#            self.neg.add(content)
#        f.close()
        
        with open(os.path.normpath(self.corpus_path + "/corpus/all_word_20181221.json"),
                                   'r',encoding='utf-8') as json_file:
            all_word=json.load(json_file)
        self.neg = set()
        self.pos = set()
        self.neu = set()
        for word in all_word['负面词']: self.neg.add(word)
        for word in all_word['正面词']: self.pos.add(word)
        for word in all_word['中性']: self.neu.add(word)

    def fit(self, X, y=None):
        return self

    def getcnt(self,x):    
        words = x.split()    
        return len(list(set(words)))

    def getnegcnt(self,x):
        negcnt = 0
        poscnt = 0
        neucnt = 0
        words = x.split()
        words_set=set(words)
        for w in words_set:
            if w in self.neg:
                negcnt = negcnt+1
            elif w in self.pos:
                poscnt = poscnt+1
            elif w in self.neu:
                neucnt = neucnt+1
                
        return negcnt, poscnt, neucnt
    
    def transform(self, X):
        data = []
        for x in X:
            words = x.split()
            if len(words) == 0:
                length  = 1
            else :
                length = len(words)
            negcnt, poscnt, neucnt = self.getnegcnt(x)
            data.append([len(x),self.getcnt(x),self.getcnt(x)/length,
                         negcnt,negcnt/length, poscnt,poscnt/length, 
                         neucnt,neucnt/length,])            
        return data

#%%
class StatsFeatures_tf_tendency(BaseEstimator, TransformerMixin):
    '''
    计算广发银行相关词的词频
    '''
    def __init__(self):
        self.corpus_path = os.path.dirname(os.path.abspath(__file__))        
        self.keywords = set()
        
        with open(os.path.normpath(self.corpus_path + "/corpus/all_word_20181221.json"),
                                   'r',encoding='utf-8') as json_file:
            all_word=json.load(json_file)

        for word in all_word['负面词']: self.keywords.add(word)
        for word in all_word['正面词']: self.keywords.add(word)       
    
    def fit(self, X, y=None):
        return self 
    
    def transform(self, X):
        '''
        文本中关键词的词频
        '''                        
        col_n = len(X)
        data = {keyword:np.zeros((1, col_n)).tolist()[0] for keyword in self.keywords}
        data['关键词的个数'] = np.zeros((1, col_n)).tolist()[0]
        for index, x in enumerate(X):
            words = x.split()
            words_set = set(words)  
            keycnt = 0
            for word in words_set:
                if word in self.keywords:
                    keycnt+=1
                    data[word][index] = words.count(word)
                data['关键词的个数'][index] = keycnt
        count_data = np.transpose(np.array([t for t in data.values()]))
        return count_data    

#%%
class StatsFeatures_warn(BaseEstimator, TransformerMixin):
    
    def __init__(self):
        self.corpus_path = os.path.dirname(os.path.abspath(__file__))
        print(self.corpus_path)
        
        self.neg = set()
        f = open(os.path.normpath(self.corpus_path + "/corpus/neg_words.txt"),
                 "r+", encoding='UTF-8')
        for content in f:
            self.neg.add(content)
        f.close()

    def fit(self, X, y=None):
        return self

    def getcnt(self,x):    
        words = x.split()    
        return len(list(set(words)))

    def getnegcnt(self,x):
        negcnt = 0
        words = x.split()
        words_set=set(words)
        for w in words_set:
            if w in self.neg:
                negcnt = negcnt+1
        return negcnt
    
    def transform(self, X):
        data = []
        for x in X:
            words = x.split()
            if len(words) == 0:
                length  = 1
            else :
                length = len(words)
            data.append([len(x),self.getcnt(x),self.getcnt(x)/length,
                         self.getnegcnt(x),self.getnegcnt(x)/length])            
        return data
