#!/usr/bin/python
# -*- coding:utf-8 -*-
#%%
from sklearn.base import BaseEstimator, TransformerMixin
import random
import datetime
import sqlite3
import pymysql
import logging.config
import numpy as np

# 日志记录
logging.config.fileConfig("conf/logger.conf")
logger = logging.getLogger("rotating")

#%%
class mysql_memory_db():
    '''
    1 定时删除mysql中超过时间的数据;
    2 定时将内存数据库中的数据写入mysql，并清空内存数据库
    
    逻辑：相似度计算时只与内存数据库中比较，一条数据同时写入mysql、内存数据库。
        同时删除mysql和内存数据库中过期数据。
    
    '''  
    def __init__(self, day_n = 15):
        self.day_n = day_n # 不含，前多少天的数据删除
#        today_str = datetime.datetime.today().strftime("%Y-%m-%d")
        self.day_del = datetime.datetime.today() - datetime.timedelta(days=day_n)
        self.day_str = self.day_del.strftime("%Y-%m-%d")  
#        self.db_path = 'memory_db/circ_signatures_memory_%s.db'%today_str
        self.db_path = 'memory_db/circ_signatures_memory.db'
        self.table_list = [['wise_web_signatures_small', 800],
                           ['wise_web_signatures_middle', 1200],
                           ['wise_web_signatures_big', 1600]]   
        
    def get_conn_mysql(self):
        # 打开数据库连接  内网: 10.80.88.73   外网: 47.95.148.133
        try :
            mysql_conn = pymysql.connect(host='10.80.88.73', user='wisedb', 
                                         passwd='Wi$eWeb123', db='text_signatures', 
                                         charset='utf8', port=5718)
        except :
            mysql_conn = pymysql.connect(host='47.95.148.133', user='wisedb', 
                                         passwd='Wi$eWeb123', db='text_signatures', 
                                         charset='utf8', port=5718)  
        return mysql_conn
    
    def get_conn_memory(self):
        # 连接内存数据库
        memory_conn = sqlite3.connect(self.db_path)    
        memory_conn.execute("PRAGMA busy_timeout = 30000") # 30 s
        
        return memory_conn
    
    def creat_table(self):
        try :            
            mysql_conn = self.get_conn_mysql()
            mysql_cur = mysql_conn.cursor()
            memory_conn = self.get_conn_memory()
            memory_cur = memory_conn.cursor()
            
            for [table_name, sig_len] in self.table_list:
                sql_create = 'create table if not exists %s ( \
                    id INTEGER PRIMARY KEY, \
                    publishtime VARCHAR(12), \
                    signatures VARCHAR(%s))'%(table_name, sig_len)
                
                mysql_cur.execute(sql_create)
                mysql_conn.commit()
                memory_cur.execute(sql_create)
                memory_conn.commit()
        finally :
            mysql_conn.close()            
            memory_conn.close()

    def del_db_data(self):
        '''
        删除mysql、内存数据库中超过时间的数据
        先处理内存数据库，再处理mysql
        '''
        try :
            mysql_conn = self.get_conn_mysql()
            mysql_cur = mysql_conn.cursor()
            memory_conn = self.get_conn_memory()
            memory_cur = memory_conn.cursor()
            
            for [table_name, sig_len] in self.table_list:
                try :
                    logger.info('- memeory: %s'%table_name)
                    logger.info('-- before del: ')
                    sql_sel = 'select publishtime, count(id) from {0} group by publishtime'.format(table_name)
                    memory_cur.execute(sql_sel)   
                    logger.info(memory_cur.fetchall())
                    
                    sql_del = "delete from {0} \
                                where publishtime < '{1}'".format(table_name, self.day_str)            
                    memory_cur.execute(sql_del)
                    memory_conn.commit()
                    
                    logger.info('-- after del: ')
                    sql_sel = 'select publishtime, count(id) from {0} group by publishtime'.format(table_name)
                    memory_cur.execute(sql_sel)   
                    logger.info(memory_cur.fetchall())
                except Exception as e:
                    logger.error('- memeory error: %s'%e)
                    continue
                
            for [table_name, sig_len] in self.table_list:
                try :
                    logger.info('-- mysql: %s'%table_name)
                    logger.info('---- before del: ')
                    sql_sel = 'select publishtime, count(id) from {0} group by publishtime'.format(table_name)
                    mysql_cur.execute(sql_sel)   
                    logger.info(mysql_cur.fetchall())
                    
                    sql_del = "delete from {0} \
                                where publishtime < '{1}'".format(table_name, self.day_str)            
                    
                    mysql_cur.execute(sql_del)
                    mysql_conn.commit()
    
                    logger.info('---- after del: ')
                    sql_sel = 'select publishtime, count(id) from {0} group by publishtime'.format(table_name)
                    mysql_cur.execute(sql_sel)   
                    logger.info(mysql_cur.fetchall())
                except Exception as e:
                    logger.error('- mysql error: %s'%e)
                    continue
                
        finally :
            mysql_conn.close()
            memory_conn.close()
            
    def update_memory_by_mysql(self):
        '''
        程序启动时，使用mysql中的数据更新本地的内存数据库，以保持数据一致
        '''
        logger.info('starting update_memory_by_mysql')
        try :
            mysql_conn = self.get_conn_mysql()
            mysql_cur = mysql_conn.cursor()
            memory_conn = self.get_conn_memory()
            memory_cur = memory_conn.cursor()
            
            for [table_name, sig_len] in self.table_list:
                
                try :
                    # 读取 mysql
                    sql_sel = 'select * from {0}'.format(table_name)
                    mysql_cur.execute(sql_sel)
                    table_data = mysql_cur.fetchall()
                    logger.info("process mysql table: %s, num:%s"%(table_name, len(table_data)))
                    
                    # 写入内存数据库
                    sql_sel = 'select count(id) from {0}'.format(table_name)                    
                    sel_num = memory_cur.execute(sql_sel).fetchall()
                    logger.info("process memory select table: %s, num:%s"%(table_name, sel_num[0][0]))
                    
                    sql_truncate = 'delete from {0}'.format(table_name)
                    memory_cur.execute(sql_truncate)
                    memory_conn.commit()
                    sel_num = memory_cur.execute(sql_sel).fetchall()
                    logger.info("process memory delete table: %s, num:%s"%(table_name, sel_num[0][0]))

                    insert_memory_sql = "INSERT INTO {0} VALUES (?, ?, ?);".format(table_name)
                    memory_cur.executemany(insert_memory_sql, table_data) # 批量插入
                    memory_conn.commit()
                    sel_num = memory_cur.execute(sql_sel).fetchall()
                    logger.info("process memory insert table: %s, num:%s"%(table_name, sel_num[0][0]))
                except Exception as e:
                    logger.error('- update_memory_by_mysql error: %s'%e)
                    continue
                
        finally :
            mysql_conn.close()
            memory_conn.close()
        logger.info('end update_memory_by_mysql')
            
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
        self.neg = set()
        f = open("corpus/neg_words.txt","r+", encoding='UTF-8')
        for content in f:
            self.neg.add(content.strip())
        f.close()
        
        self.company = set() # 公司
        f = open("corpus/insurance_company_20180803.txt","r+", encoding='UTF-8')
        for content in f:
            self.company.add(content.strip())
        f.close()

        self.regulators = set() # 监管机构及领导
        f = open("corpus/insurance_regulators_20180804.txt","r+", encoding='UTF-8')
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
        self.neg = set()
        f = open("corpus/neg_words.txt","r+", encoding='UTF-8')
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
        self.neg = set()
        f = open("corpus/neg_words.txt","r+", encoding='UTF-8')
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