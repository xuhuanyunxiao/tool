#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

dir_path = os.path.dirname(os.path.abspath(__file__))
stopwords_dir = dir_path + '/stopwords_list/'
coprus_save_filename = dir_path + '/corpus/stopwords_20180904.txt'

def update_stopwords(stopwords_dir, coprus_save_filename):
    stopwords_filelist = os.listdir(stopwords_dir)
    stopwords_list = set()
    for file_name in stopwords_filelist:    
        len_1 = len(stopwords_list)
        file_path = stopwords_dir + file_name
        fid = open(file_path, "r+", encoding='UTF-8')
        num = 0
        for f in fid:
            num+=1
            stopwords_list.add(f)
        fid.close()
        print('process file_name: %s, word num: %s'%(file_name, num))
        print('  stopwords_list num: %s, add num: %s'%(len(stopwords_list), 
                                                       len(stopwords_list) - len_1))
        
    f = open(coprus_save_filename, "w+", encoding='UTF-8')
    for data in stopwords_list:
        f.write(data)
    f.close()


#update_stopwords(stopwords_dir, coprus_save_filename)















