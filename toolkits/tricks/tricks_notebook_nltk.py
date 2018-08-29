# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 10:49:30 2017

@author: xh
"""

#%% -----------------     jupyter notebook  ----------------------

# 自动输出 HTML 文件
def output_HTML(read_file, output_file):
    from nbconvert import HTMLExporter
    import codecs
    import nbformat
    exporter = HTMLExporter()
    # read_file is '.ipynb', output_file is '.html'
    output_notebook = nbformat.read(read_file, as_version=4)
    output, resources = exporter.from_notebook_node(output_notebook)
    codecs.open(output_file, 'w', encoding='utf-8').write(output)
        
html_file_folder = result_folder + '\\sdm_2\\html_files'
if not os.path.exists(html_file_folder):
    os.makedirs(html_file_folder)

current_file = pyfile_folder + '\\notebook\\sdm_2_4_其他.ipynb'
output_file = html_file_folder + '\\sdm_2_4_其他.html' 
output_HTML(current_file, output_file)


# 忽略警告
import warnings
warnings.filterwarnings('ignore')

#%% -----------------     NLTK  ----------------------
# ——nltk.corpus    获取语料库。
# ——————语料库和词典的标准化接口
# ——nltk.tokenize,nltk.stem    字符串处理
# ——————分词，句子分解，提取主干
# ——nltk.collocations    搭配探究
# ——————t检验，卡方检验，点互信息
# ——nltk.tag  词性标识符
# ——————n-gram，backoff，Brill，HMM，TnT
# ——nltk.classify,nltk.cluster    分类
# ——————决策树，最大熵，朴素贝叶斯，EM，k-means
# ——nltk.chunk    分块
# ——————正则表达式，n-gram，命名实体
# ——nltk.parse    解析
# ——————图表，基于特征，一致性，概率性，依赖项
# ——nltk.sem,nltk.inference    语义解释
# ——————λ演算，一阶逻辑，模型检验
# ——nltk.metrics    指标评测
# ——————精度，召回率，协议系数
# ——nltk.probability    概率与估计
# ——————频率分布，平滑概率分布
# ——nltk.app,nltk.chat     应用
# ——————图形化的关键词排序，分析器，WordNet查看器，聊天机器人
# ——nltk.toolbox     语言学领域的工作
# ——————处理SIL工具箱格式的数据

# Sentence Tokenize（分割句子）  ----------------------
from nltk.tokenize import sent_tokenize  
sent_tokenize_list = sent_tokenize(text[0])
sent_tokenize_list

# Word Tokenize(分割单词)  ----------------------
from nltk.tokenize import word_tokenize  
word_list = word_tokenize(sent_tokenize_list[0])
print(word_list)
print()
word_tokenize_list = word_tokenize(text[0])  
print(word_tokenize_list)  

# Part-Of-Speech Tagging and POS Tagger(对词进行标注)  ----------------------
# lemmatization在词性标注后效果比较好
# 进行词性分析，去掉动词、助词等
from nltk.tokenize import word_tokenize
from nltk import pos_tag  #tokens是句子分词后的结果，同样是句子级的标注
print('-- 1 ', sent_tokenize_list[0])
word_tokenize_list = word_tokenize(sent_tokenize_list[0])  
print('-- 2 ', word_tokenize_list)   
pos_tag = pos_tag(word_tokenize_list)  
print('-- 3 ', pos_tag)  

# NLTK词性：直接使用“nltk.help.upenn_tagset()”查看官方英文说明
# 标记 含义 例子
# CC 连词 and, or,but, if, while,although
# CD 数词 twenty-four, fourth, 1991,14:24
# DT 限定词 the, a, some, most,every, no
# EX 存在量词 there, there's
# FW 外来词 dolce, ersatz, esprit, quo,maitre
# IN 介词连词 on, of,at, with,by,into, under
# JJ 形容词 new,good, high, special, big, local
# JJR 比较级词语 bleaker braver breezier briefer brighter brisker
# JJS 最高级词语 calmest cheapest choicest classiest cleanest clearest
# LS 标记 A A. B B. C C. D E F First G H I J K
# MD 情态动词 can cannot could couldn't
# NN 名词 year,home, costs, time, education
# NNS 名词复数 undergraduates scotches
# NNP 专有名词 Alison,Africa,April,Washington
# NNPS 专有名词复数 Americans Americas Amharas Amityvilles
# PDT 前限定词 all both half many
# POS 所有格标记 ' 's
# PRP 人称代词 hers herself him himself hisself
# PRP$ 所有格 her his mine my our ours
# RB 副词 occasionally unabatingly maddeningly
# RBR 副词比较级 further gloomier grander
# RBS 副词最高级 best biggest bluntest earliest
# RP 虚词 aboard about across along apart
# SYM 符号 % & ' '' ''. ) )
# TO 词to to
# UH 感叹词 Goodbye Goody Gosh Wow
# VB 动词 ask assemble assess
# VBD 动词过去式 dipped pleaded swiped
# VBG 动词现在分词 telegraphing stirring focusing
# VBN 动词过去分词 multihulled dilapidated aerosolized
# VBP 动词现在式非第三人称时态 predominate wrap resort sue
# VBZ 动词现在式第三人称时态 bases reconstructs marks
# WDT Wh限定词 who,which,when,what,where,how
# WP WH代词 that what whatever
# WP$ WH代词所有格 whose
# WRB WH副词

# Stemming / Lemmatization 词干提取/词形还原  ----------------------
# 先词形还原后词干提取，归一化不同词性的单词。仅词形还原可能会有复数还原不全的问题。
# 词干提取(stemming)和词型还原(lemmatization)是英文文本预处理的特色。
# 两者其实有共同点，即都是要找到词的原始形式。
# 只不过词干提取(stemming)会更加激进一点，它在寻找词干的时候可以会得到不是词的词干。比如”imaging”的词干可能得到的是”imag”, 并不是一个词。而词形还原则保守一些，它一般只对能够还原成一个正确的词的词进行处理。个人比较喜欢使用词型还原而不是词干提取。
# 在nltk中，做词干提取的方法有PorterStemmer，LancasterStemmer和SnowballStemmer。
# 个人推荐使用SnowballStemmer。这个类可以处理很多种语言，当然，除了中文。
from nltk.stem import SnowballStemmer
stemmer = SnowballStemmer("english") # Choose a language
stemmer.stem("countries") # Stem a word

import nltk  
sent1='The cat is walking in the bedroom.'  
sent2='A dog was running across the kitchen.'  
tokens_1=nltk.word_tokenize(sent1)  
print (tokens_1)  
stemmer = nltk.stem.PorterStemmer()  
stem_1 = [stemmer.stem(t) for t in tokens_1]  
print(stem_1) 

# 如果是做词型还原，则一般可以使用WordNetLemmatizer类，即wordnet词形还原方法，Lemmatization 把一个任何形式的语言词汇还原为一般形式，标记词性的前提下效果比较好。
# 在实际的英文文本挖掘预处理的时候，建议使用基于wordnet的词形还原就可以了。
from nltk.stem import WordNetLemmatizer
wnl = WordNetLemmatizer()
print(wnl.lemmatize('countries'))  

# Remove Stop Words 去除停用词  ----------------------
from nltk.corpus import stopwords   #去停用词
print('-- 1 ', sent_tokenize_list[0])
word_tokenize_list = word_tokenize(sent_tokenize_list[0])  
print('-- 2 ', word_tokenize_list)  
cachedStopWords = stopwords.words("english")
print(len(cachedStopWords))
filtered = [w for w in word_tokenize_list if (w not in cachedStopWords)]    
print(filtered)    
