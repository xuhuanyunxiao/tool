#!/usr/bin/python
# -*- coding:utf-8 -*-
#%%
from sklearn.base import BaseEstimator, TransformerMixin

#%% 
class StatsFeatures(BaseEstimator, TransformerMixin):
    
    def __init__(self):
        self.neg = set()
        f = open("corpus/neg_words.txt","r+", encoding='UTF-8')
        for content in f:
            self.neg.add(content)
        f.close()

    def fit(self, X, y=None):
        return self

    def getcnt(self,x):        
        return len(list(set(x)))

    def getnegcnt(self,x):
        negcnt = 0
        words = x.split()
        for w in words:
            if w in self.neg:
                negcnt = negcnt+1
        return negcnt
    
    def transform(self, X):
        data = []
        for x in X:
            if len(x) == 0:
                length  = 1
            else :
                length = len(x)
            data.append([len(x),self.getcnt(x),self.getcnt(x)/length,
                         self.getnegcnt(x),self.getnegcnt(x)/length])            
        return data

#%%
class StatsFeatures_cor(BaseEstimator, TransformerMixin):
    
    def __init__(self):
        self.neg = set()
        f = open("corpus/neg_words_20180704.txt","r+", encoding='UTF-8')
        for content in f:
            self.neg.add(content.strip())
        f.close()
        
        self.company = set() # 公司
        f = open("corpus/bank_company_20180814.txt","r+", encoding='UTF-8')
        for content in f:
            self.company.add(content.strip())
        f.close()

        self.regulators = set() # 监管机构及领导
        f = open("corpus/bank_regulators_20180815.txt","r+", encoding='UTF-8')
        for content in f:
            self.regulators.add(content.strip())
        f.close()    
        
        #初始化字典liwc
        self.liwc = {} 
        f2 = open("corpus/scliwc.txt",'r', encoding = 'gb18030')
        for ii in f2:     #ii在scliwc.txt中循环
            i = ii.strip().split() 
            self.liwc[i[0]] = i[1:len(i)]
        f2.close      
        
        self.category = set()
        for i in list(self.liwc.values()):
            for j in i:
                self.category.add(j)         
        
    def fit(self, X, y=None):
        return self

    def getcnt(self,x):        
        return len(list(set(x)))

    def getnegcnt(self,x):
        negcnt = 0
        words = x.split()
        for w in words:
            if w in self.neg:
                negcnt = negcnt+1
        return negcnt
    
    def getorgcnttf(self,x):
        companycnt=0
        companytf=0
        regcnt = 0
        regtf = 0
        
        words = x.split()
        words_set=set(words)
        for w in words_set:
            if w in self.company:
                companycnt = companycnt+1
                companytf=companytf+words.count(w)
                
            if w in self.regulators:
                regcnt = regcnt+1
                regtf=regtf+words.count(w)            
                
        return companycnt, companytf, regcnt, regtf
    
    def transform(self, X):
        data = []
        for x in X:
            if len(x) == 0:
                length  = 1
            else :
                length = len(x)
                
            companycnt, companytf, regcnt, regtf=self.getorgcnttf(x)
            
#             words = x.split()
#             psy = []
#             for w in words:
#                 if w in self.liwc: #是否liwc字典包含分词结果列表words的哪些分词
#                     psy += self.liwc[w] 
            
#             cat_tf = []
#             for cat in self.category:
#                 cat_tf.append(psy.count(cat)) 
                
            data.append([len(x),self.getcnt(x),self.getcnt(x)/length,
                         self.getnegcnt(x),self.getnegcnt(x)/length,
                         companycnt, companytf, regcnt, regtf]) #  + cat_tf           
        return data
    
from jieba import analyse    
def getkeywords(X, N = 1000):
    '''
    训练时生成，合并所有记录，取N个关键词
    '''
    textrank = analyse.textrank

    text_combined = ' '.join(X)
    keywords = textrank(text_combined, topK = N)
    print('keywords num: ', len(keywords))
    if len(keywords) < N : 
        N  = len(keywords)

    if keywords:
        f = open("corpus/keywords.txt","w+", encoding='UTF-8')
        for content in keywords:
            content = content.strip()
            f.write(content + '\n')
        f.close()    
    
class Statskeywords(BaseEstimator, TransformerMixin):
    
    def __init__(self, topk = 100):
        self.topk = topk
        
        self.keywords = set()
        f = open("corpus/keywords.txt","r+", encoding='UTF-8')
        num = 0
        for content in f:
            if num < topk:
                self.keywords.add(content.strip().replace('\n', ''))
            num += 1
        f.close() 
    
    def fit(self, X, y=None):
        return self 
    
    def transform(self, X):
        '''
        文本中关键词的词频
        '''                        
        data = []
        for x in X:
            words = x.split()
            word_tf = []
            keycnt = 0
            for kw in self.keywords:
                word_tf.append(words.count(kw)) # 各个关键词的词频
                if kw in words:keycnt+=1
            word_tf.append(keycnt) # 关键词的个数             
                
            data.append(word_tf)       
            
        return data        




