#!/usr/bin/python
# -*- coding:utf-8 -*-
from __future__ import division
import re
import jieba
from string import digits

stopwords = {}
stw = open("corpus/stop_words_cor.txt", encoding='UTF-8')
for ws in stw:
    ws = ws.replace("\n", "")
    ws = ws.replace("\r", "")
    stopwords[ws] = 1
stw.close()

#jieba.load_userdict('corpus/company.txt')
#jieba.load_userdict('corpus/user_dict.txt')
#jieba.load_userdict('corpus/bank_dict.txt')
jieba.load_userdict('corpus/insurance_dict_20180803.txt')

def handle_contents(l_contents):
    # print('。。。 分词 。。。')
    lines = []
    for line in l_contents:
        lines.append(handle_content(line))
    return lines

def handle_content(content):
    content = str(content)
    raw = content.strip()
    line = ""
    if raw != "":
        # 1 清理字符串
        raw = clear_sen(raw)

        # 2 分词
        # 去掉长度小于3、去掉数字、去掉标点符号
        word_list = filter(lambda x: len(x) > 0, map(etl, jieba.cut(raw, cut_all=False)))
        ll = list(word_list)

        # 3 去停用词
        for wd in ll:
        	if wd not in stopwords:
        		line = line + wd.replace(' ', '') + " "
    return line

def clear_sen(sent):
    sent = sent.replace("\n", "")
    sent = sent.replace('\r','')
    sent = sent.replace('\t','')
    sent = sent.replace('\r\n','')
    sent = sent.replace("|", "")
    sent = sent.replace("——", "")
    reobj = re.compile('//@(.*?)[:\s]')
    sent = reobj.sub("", sent)
    reobj = re.compile("@(.*?)[:\s]")
    sent = reobj.sub("", sent)
    reobj = re.compile(r"\[[^\[\]]*?\]")
    sent = reobj.sub("", sent)
    sent = re.sub(r'[a-z]*', '', sent)

    sent = sent.replace("，", ",")
    sent = sent.replace("。", ".")
    sent = sent.replace("！", "!")
    sent = sent.replace("？", "?")
    reobj = re.compile("//(.*?)[:\s]")
    sent = reobj.sub("", sent)
    sent = re.sub(r'[a-z]*', '', sent)
    return sent

def etl(s):  
    # 去除标点和特殊字符
    regex = re.compile(r"[^\u4e00-\u9f5aa-zA-Z0-9]")
    s = regex.sub('', s)

    # 去除字符中的数字
    remove_digits = str.maketrans('', '', digits)
    res = s.translate(remove_digits)
    return res


