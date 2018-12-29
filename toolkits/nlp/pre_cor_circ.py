#!/usr/bin/python
# -*- coding:utf-8 -*-
from __future__ import division
import jieba
from string import digits
import os
dir_path = os.path.dirname(os.path.abspath(__file__))

# from langconv import *
from toolkits.nlp.langconv import *
from toolkits.setup.specific_func import Traditional2Simplified
from toolkits.nlp import utils

jieba.load_userdict(os.path.normpath(dir_path + '/corpus/insurance_dict_20180803.txt'))

def handle_contents(contents):
    # print('。。。 分词 。。。')
    content_list = []
    for content in contents:
        content = str(content)
        content = Traditional2Simplified(content) # 繁体字转简体字
        content_list.append(utils.handle_content(content))
    return content_list


