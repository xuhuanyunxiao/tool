#!/usr/bin/python
# -*- coding:utf-8 -*-
#%%
from sklearn.base import BaseEstimator, TransformerMixin
import random
import numpy as np
import os
            
#%%
def pickRandomCoeffs(k, maxShingleID):
    '''
    minhash：生成系数
    # Our random hash function will take the form of:
    #   h(x) = (a*x + b) % c
    # Where 'x' is the input value, 'a' and 'b' are random coefficients, and 'c' is
    # a prime number just greater than maxShingleID.

    # Generate a list of 'k' random coefficients for the random hash functions,
    # while ensuring that the same value does not appear multiple times in the 
    # list.    
    '''
    
    # Create a list of 'k' random values.
    randList = []

    while k > 0:
        # Get a random shingle ID.
        randIndex = random.randint(0, maxShingleID) 

        # Ensure that each random number is unique.
        while randIndex in randList:
              randIndex = random.randint(0, maxShingleID) 

        # Add the random number to the list.
        randList.append(randIndex)
        k = k - 1

    return randList

#maxShingleID = 2**32-1
#nextPrime = 4294967311
#    
#numHashes = 75
#coeffA = pickRandomCoeffs(numHashes, maxShingleID)
#coeffB = pickRandomCoeffs(numHashes, maxShingleID)
#
#f = open('corpus/minhash_coeff_A_B_big_20180713.txt', 'w+', encoding = 'utf-8')
#
#coeff_A_B = [['coeffA'] + coeffA, ['coeffB'] + coeffB]
#
#for a, b in zip(coeff_A_B[0], coeff_A_B[1]):
#    f.write(str(a) + '\t' + str(b) + '\n')
#f.close()

#%% 
class StatsFeatures_cor(BaseEstimator, TransformerMixin):
    
    def __init__(self):
        self.corpus_path = os.path.dirname(os.path.abspath(__file__))
        print(self.corpus_path)
        
        self.neg = set()
        f = open(os.path.normpath(self.corpus_path + "/corpus/neg_words.txt"),
                 "r+", encoding='UTF-8')
        for content in f:
            self.neg.add(content.strip())
        f.close()
        
        self.company = set() # 公司
        f = open(os.path.normpath(self.corpus_path + "/corpus/insurance_company_20180803.txt"),
                 "r+", encoding='UTF-8')
        for content in f:
            self.company.add(content.strip())
        f.close()

        self.regulators = set() # 监管机构及领导
        f = open(os.path.normpath(self.corpus_path + "/corpus/insurance_regulators_20180804.txt"),
                 "r+", encoding='UTF-8')
        for content in f:
            self.regulators.add(content.strip())
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
        orgcnt = [companycnt, companytf, regcnt, regtf]        
        return orgcnt
    
    def transform(self, X):
        data = []
        for x in X:
            words = x.split()
            if len(words) == 0:
                length  = 1
            else :
                length = len(words)

            data.append([len(x),self.getcnt(x),self.getcnt(x)/length, 
                         self.getnegcnt(x),self.getnegcnt(x)/length] + self.getorgcnttf(x))    
        return data

#%%
class Statskeywords_cor(BaseEstimator, TransformerMixin):
    
    def __init__(self, topk = 100, types = 'circ'):
        self.corpus_path = os.path.dirname(os.path.abspath(__file__))
        print(self.corpus_path)
        
        self.topk = topk
        
        self.keywords = set()
        f = open(os.path.normpath(self.corpus_path + "/corpus/keywords_i_%s.txt"%types),
                 "r+", encoding='UTF-8')
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
class StatsFeatures_tendency(BaseEstimator, TransformerMixin):
    
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
    
#%%
class StatsFeatures_tf_picc(BaseEstimator, TransformerMixin):
    '''
    计算中国人保中交通与环保相关词的词频
    '''
    def __init__(self):
        self.corpus_path = os.path.dirname(os.path.abspath(__file__))        
        self.keywords = set()
        f = open(os.path.normpath(self.corpus_path + "/corpus/environment.txt"),
                 "r+", encoding='UTF-8')
        for content in f:
            for w in content.strip().replace('\n', '').replace('\ufeff', '').split():
                self.keywords.add(w)
        f.close() 
        
        f = open(os.path.normpath(self.corpus_path + "/corpus/traffic.txt"),
                 "r+", encoding='UTF-8')
        for content in f:
            for w in content.strip().replace('\n', '').replace('\ufeff', '').split():
                self.keywords.add(w)
        f.close()         

        f = open(os.path.normpath(self.corpus_path + "/corpus/traffic_environment.txt"),
                 "r+", encoding='UTF-8')
        for content in f:
            for w in content.strip().replace('\n', '').replace('\ufeff', '').split():
                self.keywords.add(w)
        f.close() 
        
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
class StatsFeatures_tf_clic(BaseEstimator, TransformerMixin):
    '''
    计算广发银行相关词的词频
    '''
    def __init__(self):
        self.corpus_path = os.path.dirname(os.path.abspath(__file__))        
        self.keywords = set()
        f = open(os.path.normpath(self.corpus_path + "/corpus/clic_org.txt"),
                 "r+", encoding='UTF-8')
        for content in f:
            for w in content.strip().replace('\n', '').replace('\ufeff', '').split():
                self.keywords.add(w)
        f.close() 
        
        f = open(os.path.normpath(self.corpus_path + "/corpus/clic_bank_guangfa.txt"),
                 "r+", encoding='UTF-8')
        for content in f:
            for w in content.strip().replace('\n', '').replace('\ufeff', '').split():
                self.keywords.add(w)
        f.close()         
    
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
#a = StatsFeatures_tf()


