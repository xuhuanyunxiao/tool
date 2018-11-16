#!/usr/bin/python
# -*- coding:utf-8 -*-
from __future__ import division
import re
import jieba
from string import digits
import os
dir_path = os.path.dirname(os.path.abspath(__file__))


def title_content_label(filepath):
	'''
	导入预处理后的数据 txt文件
	'''
    title = []
    filename = filepath + 'titles.txt'
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

class DenseTransformer(TransformerMixin):
	'''
	spare data to dense data
	'''
    def transform(self, X, y=None, **fit_params):
        return X.todense()

    def fit_transform(self, X, y=None, **fit_params):
        self.fit(X, y, **fit_params)
        return self.transform(X)

    def fit(self, X, y=None, **fit_params):
        return self



