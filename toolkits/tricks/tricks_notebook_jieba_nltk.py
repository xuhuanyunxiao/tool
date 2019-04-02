# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 10:49:30 2017

@author: xh
"""

#%% -----------------     jupyter notebook  ----------------------
# 键盘快捷方式的方法，以及学习它们的方便方法是使用：Cmd + Shift + P
# （或者在Linux和Windows上使用Ctrl + Shift + P）。 
# 此对话框可帮助你按名称运行任何命令 - 
# 如果你不知道某个操作的键盘快捷方式，
# 或者您想要执行的操作没有键盘快捷键，则可以使用该对话框。

# 在最后一行阻止函数的输出是很方便的，例如绘图时。 要做到这一点，你只需在最后添加一个分号

?str.replace() # 帮助

# 多个指针同步编辑，类似Sublime Text编辑器。按下Alt键并拖拽鼠标即可实现。

# %符号是jupyter notebook里的魔术命令 ----------------------
# ％env：设置环境变量
#Running %env without any arguments
#lists all environment variables
#The line below sets the environment
#variable OMP_NUM_THREADS
%env OMP_NUM_THREADS=4
env:OMP_NUM_THREADS=4

# ％run：执行python代码
# ％run可以从.py文件中执行python代码，鲜为人知的是，它也可以执行其他jupyter notebooks，相当有用。
# 请注意，使用％run与导入python模块不同。
#this will execute and show the output from
#all code cells of the specified notebook
%run ./two-histograms.ipynb

# ％load：从外部脚本插入代码
# 这将用外部脚本替换单元格的内容。 你可以使用计算机上的文件作为源，也可以使用URL。
#Before Running
%load ./hello_world.py
# After Running
# %load ./hello_world.py
if __name__ == "__main__":
    print("Hello World!")
# Hello World!

# ％store：在笔记本之间传递变量
# ％store命令可以让你在两个不同的文件之间传递变量。
data = 'this is the string I want to pass to different notebook'
%store data
del data # This has deleted the variable
Stored 'data' (str)
# new
%store -r data
print(data)
# this is the string I want to pass to different notebook

# ％who：列出全局范围的所有变量
# 没有任何参数的％who命令将列出全局范围中存在的所有变量。 
# 传递像str这样的参数将仅列出该类型的变量。
one = "for the money"
two = "for the show"
three = "togetready nowgocat go"
%who str
# one three two

# 有两个IPython Magic命令对时间有效 - %%time和％timeit。
# %%time会给你关于单元中的代码的单一运行的信息。
%%time
import time
for_ in range(1000):
    time.sleep(0.01)# sleepfor0.01seconds

%timeit numpy.random.normal(size=100)

# %% writefile magic将该单元格的内容保存到外部文件中。 
# ％pycat会做相反的处理，并显示（在弹出窗口中）外部文件高亮内容
%%writefile pythoncode.py
%pycat pythoncode.py

# %prun: Show how much time your program spent in each function
%prun some_useless_slow_function()

# ％pdb进行调试
# 输出Retina notebooks的高分辨率绘图
%config InlineBackend.figure_format = 'retina'

# 编写LaTeX ----------------------
# 当你在Markdown单元格中编写LaTeX时，使用MathJax将其渲染为公式。
# $$ P(A mid B) = frac{P(B mid A) , P(A)}{P(B)} $$

# 运行不同语言 ----------------------
%%bash
%%HTML
%%python2
%%python3
%%ruby
%%perl
%%R

%%bash
for i in {1..5}
do
   echo "$i"
done

# ！符号是执行shell的命令 ----------------------
!ls
!apt-get install graphviz
!pip install pydotplus

# 自动输出 HTML 文件  ----------------------
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


# 显示文件夹中文件  ----------------------
%env LS_COLORS = None 
!tree --charset ascii  data/dogcat/


# 忽略警告  ----------------------
import warnings
warnings.filterwarnings('ignore')

# 自动重新加载更改的模块  ----------------------
%load_ext autoreload
%autoreload 2

%matplotlib inline

#   ----------------------
notebook info
c.NotebookApp.ip = '192.168.30.220'
c.NotebookApp.notebook_dir = u'/data/python_apps/jupyter_notebook'
c.NotebookApp.open_browser = False
c.NotebookApp.password = u'sha1:b1f662173fa0:59a209152386bdffe31a4c104b1bf217dbdd2f49'
c.NotebookApp.port = 9000

# 启动  ----------------------
jupyter notebook --config /root/.jupyter/xh_jupyter_notebook_config.py --allow-root
# 后台挂起
nohup jupyter notebook --config /root/.jupyter/xh_jupyter_notebook_config.py --allow-root &
# 关闭notebook
lsof -i:9000  查看PID
kill -9 pid

# 本地
http://192.168.30.220:9000
123456

# 安装扩展  ----------------------
pip3 install jupyter_contrib_nbextensions
jupyter contrib nbextension install --user

# 如果没有出现扩展界面，可直接设置扩展
http://192.168.30.220:9000/nbextensions?nbextension=varInspector/main


# 创建幻灯片文件  ----------------------
# 在保存的目录之下，执行下面命令：
jupyter nbconvert add_and_warn_4.ipynb --to slides --post serve
jupyter nbconvert --to slides --ServePostProcessor.port=8910 --post serve add_and_warn_4.ipynb

# 要在notebook创建幻灯片文件，你需要使用 nbconvert:
jupyter nbconvert notebook.ipynb --to slides

# 希望转换后立刻看见结果，使用：
jupyter nbconvert notebook.ipynb --to slides --post serve
jupyter nbconvert add_and_warn_4.ipynb --to slides --reveal-prefix reveal.js
jupyter nbconvert add_and_warn_4.ipynb --to slides --reveal-prefix reveal.js --post serve --ServePostProcessor.port=8910


#%% -----------------     jieba  ----------------------

# 分句  ----------------------
def cut_sentences(sentence):
    '''
    中文，依据标点符号分句：。！？
    '''
    puns = frozenset(u'。！？')
    tmp = []
    for ch in sentence:
        tmp.append(ch)
        if puns.__contains__(ch):
            yield ''.join(tmp)
            tmp = []
    yield ''.join(tmp)

def cut_sentences(para):
    para = re.sub('([。！？\?])([^”])',r"\1\n\2",para) # 单字符断句符
    para = re.sub('(\.{6})([^”])',r"\1\n\2",para) # 英文省略号
    para = re.sub('(\…{2})([^”])',r"\1\n\2",para) # 中文省略号
    para = re.sub('(”)','”\n',para)   # 把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    para = para.rstrip()       # 段尾如果有多余的\n就去掉它
    #很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    return para.split("\n")

#   ----------------------
# 基于TextRank算法进行关键词抽取
from jieba import analyse
# 引入TextRank关键词抽取接口
textrank = analyse.textrank
text = "线程是程序执行时的最小单位，它是进程的一个执行流，\
    是CPU调度和分派的基本单位，一个进程可以由很多个线程组成，\
    线程间共享进程的所有资源，每个线程有自己的堆栈和局部变量。\
    线程由CPU独立调度执行，在多CPU环境下就允许多个线程同时运行。\
    同样多线程也可以实现并发操作，每个请求分配一个线程来处理。"
 
keywords = textrank(text)

# 基于TF-IDF算法进行关键词抽取
from jieba import analyse
# 引入TF-IDF关键词抽取接口
tfidf = analyse.extract_tags
keywords = tfidf(text)













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
