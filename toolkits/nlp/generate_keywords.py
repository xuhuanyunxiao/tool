#!/usr/bin/env python
# -*- coding: utf-8 -*-

#%%
from jieba import analyse
import numpy as np
from collections import Counter
import os

#%%
class generate_keywords():
    
    def __init__(self, topk = 200):
        '''
        topk: 一类则选出出现次数最高的 topk 个词，不足时有多少算多少；多类则各类都选topk个词
        '''
        self.class_key_dict = {}
        self.key_dict = {}
        self.topk = topk
        self.dir_path = os.path.dirname(os.path.abspath(__file__))
        
    def save_txt(self,save_filename):
        # save_filename = keywords.txt
        file_path = self.dir_path + "/corpus/%s"%save_filename
        print('file_path: ', file_path)
        f = open(file_path,"w+", encoding='UTF-8')
        for content in self.keywords:
            content = content.strip()
            f.write(content + '\n')
        f.close()         
        
    def gen_keywords(self, title_content):
        '''
        不分类别产生关键词，方法：textrank
        title_content: list 
        '''
        keyword_list = []
        for pre_sen in title_content:
            textrank = analyse.textrank      
            kw_list = textrank(pre_sen)
            keyword_list += kw_list
        
        keyword_freq = dict(Counter(keyword_list))
        keyword_freq_sort = sorted(keyword_freq.items(),key = lambda x:x[1],reverse = True)
        if self.topk > len(keyword_freq_sort):
            keyword_list = [kw[0] for kw in keyword_freq_sort]
        else :
            keyword_list = [kw[0] for kw in keyword_freq_sort[:self.topk]]
        self.keywords = keyword_list
        print(self.keywords[:10])
        print('keywords num: ', len(self.keywords))
        return keyword_list
    
    def gen_keywords_by_class(self, title_content, label, v_thre = None):
        '''
        依据分类类别各自生成关键词，并去除在所有类别中出现次数超过阈值的词
        title_content: list 
        label： list , 与title_content对应
        n_word: int, topk
        v_thre:int, 在所有类别中出现的次数应该低于该值，范围：0 - n_calss
        '''

        self.class_label = np.unique(label)
        print('class_label: ', self.class_label)
        print()
        print('依据类别生成关键词：')
        for index, c_label in enumerate(self.class_label):
            str_list = [m for m,n in zip(title_content, label) if n == c_label]
            keyword_list = self.gen_keywords(str_list)

            print('类别：%s -- 文本个数：%s，label个数:%s，取词个数：%s'%(c_label, len(str_list), 
                                                label.count(c_label), len(keyword_list)))
            self.class_key_dict[c_label] = keyword_list
            for key in keyword_list: # 计算在各类别中出现的次数
                if key not in self.key_dict:            
                    self.key_dict[key] = 1
                else :
                    self.key_dict[key] += 1
        
        # 统计一个词在多类中出现的次数，如果超过阈值（v_thre）则去除        
        if v_thre == None:
            v_thre = int(len(self.class_label)/2)
        else :
            v_thre = v_thre
        self.key_count_list = [k for k,v in self.key_dict.items() if v > v_thre]
        print()
        print('去除词（key_count_list）个数：', len(self.key_count_list))
        print('词典词（key_dict）个数：', len(self.key_dict.values()))
        print()
#        print(list(self.key_dict.values()))

        # 去除超过阈值（v_thre）的词
        print('前后对比：去除超过阈值的词')
        keywords = []
        for index, c_label in enumerate(self.class_label):
            keyword_list = self.class_key_dict[c_label]
            len_be = len(keyword_list)
            for k in self.key_count_list:        
                if k in keyword_list:
                    keyword_list.remove(k)
            print(keyword_list[:10])
            print('类别：%s -- 去除前：%s， 去除后：%s'%(c_label, len_be, len(keyword_list)))
            
            keywords += keyword_list
        
        self.keywords = list(set(keywords))
        print(self.keywords[:10])
        print('len(keywords): ', len(self.keywords))
#        return keywords

#%%

