#!/usr/bin/python
# -*- coding:utf-8 -*-
from __future__ import division
import re
import jieba
from string import digits

import os
dir_path = os.path.dirname(os.path.abspath(__file__))

stopwords = {}
stw = open(dir_path + "/corpus/stopwords_20180904.txt", encoding='UTF-8')
for ws in stw:
    ws = ws.replace("\n", "")
    ws = ws.replace("\r", "")
    stopwords[ws] = 1
stw.close()

# jieba.load_userdict('corpus/company.txt')
jieba.load_userdict(dir_path + '/corpus/bank_dict_20180814.txt') # 合并了 user_dict.txt
jieba.load_userdict(dir_path + '/corpus/neg_words_20180704.txt')


def handle_contents(l_contents):
    lines = []
    for line in l_contents:
        lines.append(handle_content(line))
    return lines

def handle_content(content):
    content = str(content)
    raw = content.strip()
    line = ""
    if raw != "":
        word_list_1 = []
        line = ""
        remove_words = []
        raw = clear_sen(raw)
        word_list = filter(lambda x: len(x) > 0, map(etl, jieba.cut(raw, cut_all=False)))
        ll = list(word_list)
        for wd in ll:
            if wd in stopwords:
                remove_words.append(wd)

        for l in ll:
            if not (l in remove_words):
                word_list_1.append(l)

        for wd in word_list_1:
            line = line + wd + " "
    return line



def clear_sen(sent):
    '''
    清理句子：
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

    reobj = re.compile(r"[^\u4e00-\u9f5a。！？“”，：、（）；<>]*")
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
    sent = reobj.sub("", sent)
    reobj = re.compile(r'[责任编辑|更多关于]+[ ：:\u4e00-\u9fa5]*')
    sent = reobj.sub("", sent)
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

def etl(s):  
    # 去除标点和特殊字符
    regex = re.compile(r"[^\u4e00-\u9f5aa-zA-Z0-9]")
    s = regex.sub('', s)

    # 去除字符中的数字
    # remove_digits = str.maketrans('', '', digits)
    # s = s.translate(remove_digits)
    return s
