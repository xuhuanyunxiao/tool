# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 10:07:45 2018

@author: Administrator
"""
#%%
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

import os

#%%
pyfile_folder = r'D:\XH\Python_Project\Proj_2\files'
data_folder = r'D:\XH\Python_Project\Proj_2\data'
result_folder = r'D:\XH\Python_Project\Proj_2\result'

#%%
#from pdfminer.pdfparser import PDFParser
#from pdfminer.pdfdocument import PDFDocument


file_name = 'Statistical Computing in Functional Data Analysis_ The R Package fda.pdf'
# Open a PDF document.
pdf_file = open(os.path.join(data_folder,file_name), 'rb')
parser = PDFParser(pdf_file)
document = PDFDocument(parser)
 
# Get the outlines of the document.
outlines = document.get_outlines()
for (level,title,dest,a,se) in outlines:
    print(level, title)

#%%
def parse(pdf_file):    
    #rb以二进制读模式打开本地pdf文件
#    pdf_file = open('test.pdf','rb')
    
    #创建一个pdf文档分析器
    parser = PDFParser(pdf_file)
    #创建一个PDF文档
    doc = PDFDocument(parser)
    #连接分析器 与文档对象
#    parser.set_document(doc)
#    doc.set_parser(parser)
  
    # 提供初始化密码doc.initialize("lianxipython")
    # 如果没有密码 就创建一个空的字符串
    doc.initialize("")
    
    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:        
        raise PDFTextExtractionNotAllowed
    else:
        #创建PDf资源管理器
        resource = PDFResourceManager()
        #创建一个PDF参数分析器
        laparams = LAParams()
        #创建聚合器,用于读取文档的对象
        device = PDFPageAggregator(resource,laparams=laparams)
        #创建解释器，对文档编码，解释成Python能够识别的格式
        interpreter = PDFPageInterpreter(resource,device)
        
        # 循环遍历列表，每次处理一页的内容
        # doc.get_pages() 获取page列表
        for page in doc.get_pages():          
            #利用解释器的process_page()方法解析读取单独页数
            interpreter.process_page(page)
            #使用聚合器get_result()方法获取内容
            layout = device.get_result()
            #这里layout是一个LTPage对象,里面存放着这个page解析出的各种对象
            for out in layout:                
                #判断是否含有get_text()方法，获取我们想要的文字
                if hasattr(out,"get_text"):                    
                    print(out.get_text())
                    with open('test.txt','a') as f:                        
                        f.write(out.get_text()+'\n')

#%%
if __name__ == '__main__':
  parse(pdf_file)
