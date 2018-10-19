#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import jieba
import jieba.posseg as pseg
from string import digits
#import pre_cor_circ

#%%
#from nltk.tag import StanfordNERTagger
#chi_tagger = StanfordNERTagger('D:\software\stanford_nlp\chinese.misc.distsim.crf.ser.gz',
#                               'D:\software\stanford_nlp\stanford-ner.jar')

#%%
# 加载其他自定义词典
jieba.load_userdict('corpus/insurance_dict_20180803.txt')

pos_flag = 'jsyh'

# mysql 加载实体词典
def load_mysql_dict(dictionarys): 
    print('更新字典。。。')
    for subject_word in dictionarys:
        jieba.add_word(subject_word, 100, pos_flag)
        jieba.suggest_freq(subject_word, tune = True)
#        if subject_word in ['PP平台', 'PP']:
#            print('subject_word:', subject_word)
         
def del_mysql_dict(dictionarys): 
    for subject_word in dictionarys:
        try :
            jieba.del_word(subject_word)
        except :
            continue
        
#%%
def clear_article(content):
    content = content.replace("\n", "")
    content = content.replace('\r', '')
    content = content.replace('\r\n', '')
    reobj = re.compile('//@(.*?)[:\s]')
    content = reobj.sub("", content)
    reobj = re.compile("@(.*?)[:\s]")
    content = reobj.sub("", content)
    reobj = re.compile(r"\[[^\[\]]*?\]")
    content = reobj.sub("", content)
    
    return content
            
def clear_word(word_pos):  # remove 标点和特殊字符
    regex = re.compile(r"[^\u4e00-\u9f5aa-zA-Z0-9。]")
    word = regex.sub('', word_pos.word)
    
    # 去除字符中的数字
    remove_digits = str.maketrans('', '', digits)
    word = word.translate(remove_digits)    
    word_pos.word = word
    return word_pos

#%%
def get_pos_word(sentence):
    # 获得词列表
    words_chain = set()
    if sentence == '':
        return words_chain
    else :      
        sentence = sentence.strip()
        words = filter(lambda word_pos: (len(word_pos.word) > 0) and (word_pos.flag == pos_flag), 
                                         map(clear_word, pseg.cut(sentence)))  
        words_chain = set([w.word for w in words])
                
        return words_chain

#%%
#def get_ner_org(sentence):
#    ner_org = set()
#    if sentence == '':
#        return ner_org
#    else :        
#        words_pre = pre_cor_circ.handle_content(sentence)
#        
#        for word, tag in chi_tagger.tag(words_pre.split()):
#            if (tag == 'ORGANIZATION') and (len(word) > 3):
#                ner_org.add(word)
#        return ner_org

def count_value(sentence, count_dict, weight, flag):    
    if flag == 'old':
        sentence_list = get_pos_word(sentence)
#    elif flag == 'new':
#        sentence_list = get_ner_org(sentence)
        
    if sentence_list:
        for s in sentence_list:
            if s not in count_dict:
                count_dict[s] = sentence.count(s) * weight 
            else :
                count_dict[s] = count_dict[s] + sentence.count(s) * weight 
    return count_dict

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
    
#%%
def extract_abstract(titles, contents, dictionarys):
    load_mysql_dict(dictionarys)
    org_score = []
    for title, content in zip(titles, contents):
        content = clear_article(str(content))
        sentences = [i.strip() for i in cut_sentences(content)]
        
        len_thres = 300
        old_content_dict = {}
        if len(content) > len_thres:
            content_1000 = content[:len_thres]
            content_else = content[len_thres:]  
        else :
            content_1000 = content
            content_else = '' 
        
        # ---- 人工标注出的机构： old
        # 计算title中词的值
        old_title_dict = {}
        old_title_dict = count_value(title, old_title_dict,60, 'old')       
        # 计算content中词的值  
        old_content_dict = {}
        old_content_dict = count_value(content_1000, old_content_dict,30, 'old')          
        old_content_dict = count_value(content_else, old_content_dict,10, 'old')       
        # 合并值
        if old_title_dict:
            for key,value in old_title_dict.items():
#                print(key)
                if key not in old_content_dict:
                    old_content_dict[key] = old_title_dict[key]
                else :
                    old_content_dict[key] = old_content_dict[key] + old_title_dict[key]     
        
        # ---- NER识别出的机构： new
        new_title_dict = {}
        new_content_dict = {}
        if 0:
            # 计算title中词的值                    
            new_title_dict = count_value(title, new_title_dict, 60, 'new')                   
            # 计算content中词的值            
            new_content_dict = count_value(content_1000, new_content_dict,30, 'new')          
            new_content_dict = count_value(content_else, new_content_dict,10, 'new')                     
            # 合并值
            if new_title_dict:
                for key,value in new_title_dict.items():
                    if key not in new_content_dict:
                        new_content_dict[key] = new_title_dict[key]
                    else :
                        new_content_dict[key] = new_content_dict[key] + new_title_dict[key]   
        
        # 统一名称
        standard_dict = {}
        tmp_dict = {} # 全称 与 subject_word 之间的对应
        if old_content_dict:
            old_content_dict = sorted(old_content_dict.items(), key=lambda x: x[1], reverse=True)
            old_content_dict = {k:v for k,v in old_content_dict}
            for key in old_content_dict:
                if key in dictionarys:
                    standard_key = dictionarys[key]
                else :
                    standard_key = key
                    
                if standard_key not in tmp_dict:
                    tmp_dict[standard_key] = [key]
                else :
                    tmp_dict[standard_key].append(key)
                
                if standard_key not in standard_dict:                    
                    standard_dict[standard_key] = [old_content_dict[key], 'old']
                else :
                    standard_dict[standard_key] = [standard_dict[standard_key][0] + old_content_dict[key], 'old']
                    
        if new_content_dict:
            new_content_dict = sorted(new_content_dict.items(), key=lambda x: x[1], reverse=True)
            new_content_dict = {k:v for k,v in new_content_dict}            
            for key in new_content_dict:
                if key not in dictionarys:
                    standard_key = key
                    tmp_dict[standard_key] = [key]              
                    standard_dict[standard_key] = [new_content_dict[key], 'new']  
        
        # 获取标题
        for remove_word in ['PP', 'PP平台']:
            if remove_word in standard_dict:
                standard_dict.pop(remove_word)
        
        vip_word = ''
        key_sentence = ''
        org_score_list = []
        purity = 0
        if standard_dict:
            value_list = [value[0] for value in standard_dict.values()]
            purity = int(max(value_list) / sum(value_list) * 100)
            org_score_list = sorted(standard_dict.items(), key=lambda x: x[1][0], reverse=True)              
            if len(org_score_list) > 3:
                org_score_list = org_score_list[:3]
            org_score_list = [[org_s[0]] + org_s[1] for org_s in org_score_list]
            vip_word_list = tmp_dict[org_score_list[0][0]]
#            print('org_score_list: ', org_score_list)
#            print('vip_word_list: ', vip_word_list)
            
            for vip_word in vip_word_list:
                for sentence in sentences:                
                    if vip_word in sentence:
                        key_sentence = sentence
                        break
                if key_sentence != '':
                    break
            if len(key_sentence) > 100:
                fir_last_len = 30 # 词首尾各20个字符
                if key_sentence != '':
                    loc = key_sentence.index(vip_word)
                    if loc < fir_last_len:
                        sen_fir = 0
                    else :
                        sen_fir = loc - fir_last_len
                    if len(key_sentence) - loc < fir_last_len:
                        sen_las = len(key_sentence)
                    else :
                        sen_las = loc + fir_last_len + 10
                    key_sentence = key_sentence[sen_fir:sen_las]
        org_score.append([org_score_list, [vip_word, key_sentence], purity])
    
    del_mysql_dict(dictionarys)
    return org_score

#%%
if __name__ == '__main__':
    import json
    from line_profiler import LineProfiler
    
    titles = ['监管部门拟调研P2P平台保证保险业务', 
              '建行北京分行领导来我校洽谈银校合作事宜建行北京分行领导来我校洽谈银校合作事宜建行北京分行领导来我校洽谈银校合作事宜建行北京分行领导来我校洽谈银校合作事宜建行北京分行领导来我校洽谈银校合作事宜建行北京分行领导来我校洽谈银校合作事宜建行北京分行领导来我校洽谈银校合作事宜建行北京分行领导来我校洽谈银校合作事宜建行北京分行领导来我校洽谈银校合作事宜建行北京分行领导来我校洽谈银校合作事宜建行北京分行领导来我校洽谈银校合作事宜建行北京分行领导来我校洽谈银校合作事宜建行北京分行领导来我校洽谈银校合作事宜建行北京分行领导来我校洽谈银校合作事宜建行北京分行领导来我校洽谈银校合作事宜建行北京分行领导来我校洽谈银校合作事宜建行北京分行领导来我校洽谈银校合作事宜',]
    contents = ["摘要: 上海证券报独家获悉，各财险公司于本周收到监管部门下发的《关于开展P2P平台保证保险业务书面调研的通知》。为了解保险公司P2P平台保证保险业务情况，防范P2P平台保证保险业务风险，监管部门拟对P2P平台保证保险业务 ...上海证券报独家获悉，各财险公司于本周收到监管部门下发的《关于开展P2P平台保证保险业务书面调研的通知》。为了解保险公司P2P平台保证保险业务情况，防范P2P平台保证保险业务风险，监管部门拟对P2P平台保证保险业务开展专项调研。根据书面调研事项通知，此次调研的范围，一是保险公司：是指截至2018年8月31日止，有P2P平台保证保险业务未了责任余额的保险公司。未了责任余额包括未到期余额和未决赔款金额。二是P2P平台保证保险：是指被保险人为P2P平台上的出资人，投保人既包括P2P平台上的借款人，也包括线下业务合作方推送的借款人。调研的主要内容有以下五点：一是，各财险公司开展P2P平台保证保险业务的总体情况，并填写附件（总体情况按抵质押/纯信用、个人借款人/法人借款人等维度进行分类说明，包括但不限于每类业务的占比、未了责任余额、单户最高承保限额、未到期业务的风险评估情况、应对措施等）。二是，各财险公司开展P2P平台保证保险业务的风险管控措施。按保前、保中、保后的整个业务流程进行说明，包括但不限于业务制度和系统建设、借贷资金往来安全性、风险监测、再保险、与合作方的反制措施等。三是，各财险公司开展P2P平台保证保险业务的合规情况，对照《信用保证保险业务监管暂行办法》文件中第六条、第八条至第十二条规定说明。四是，各财险公司开展P2P平台保证保险业务产品使用情况，并对照《财产保险公司保险条款和保险费率管理办法》中关于审批、备案有关规定说明。五是，各财险公司对P2P平台保证保险业务的相关监管建议。此外，根据书面调研要求，各财险公司还需提供公司与每个P2P平台的合作协议书(PDF版)；需提供P2P平台保证保险业务的已决赔款清单；需提供P2P平台保证保险业务中涉及被保险人数最多的保险合同（每个P2P平台请提供一份，包括但不限于条款、费率、投保单、保单、被保险人清单、批单等)PDF版，以及P2P平台上单户赔款金额最大的理赔完整材料(每个P2P平台请提供一份)PDF版。根据调研时间表，各财险公司要在9月10日前将调研相关材料报送至监管部门。未开展上述P2P平台保证保险业务的保险公司，也应按照相关报送路径，以正式公文形式报告监管部门。业内人士表示，近年来随着P2P潮兴起，一批保险公司和P2P平台相继开展了业务合作。但近期P2P行业的相关风险开始浮出水面，为避免成为风险的接棒者，的确有必要对P2P平台保证保险业务进行排查与整顿。蓝岛新闻网-沿海城市新闻资讯第一门户-细分推荐：懒人", 
    '本网讯 8月27日，中国建设银行北京市分行副行长孙庆文、谢东一行10人来我校就银校战略合作事宜进行洽谈，常务副校长李召虎出席洽谈会并讲话。\
                李召虎代表学校对孙庆文一行表示欢迎，感谢建设银行北京分行对学校发展的支持，并对学校的教学、科研、社会服务等方面的基本情况和取得的成果进行了重点介绍。\
                他表示，建行与学校长期开展合作，建立了很好的合作基础，并取得了积极成果。希望双方着眼未来发展，进一步开展深入战略合作，携手谋划，增强合作的生命力，逐步发展研究型合作，谋求银校共赢发展。\
                孙庆文感谢我校多年来对建行的信任和支持，并对我校的办学特色、办学水平及各方面取得的成绩表示赞扬。他说，建行与农大在校园一卡通一期、二期的合作非常融洽，\
                今年将继续深化与农大的合作，以合力建设“智慧校园”为契机，在资金和技术方面整体投入，进一步加强在金融科技领域的合作，将建行与农大的合作落地生根。\
                会上，财务处处长张树彦介绍了建设银行北京分行与我校的合作历程，并对下一步银校合作的方案进行了简要说明；双方还就合作的相关问题进行了商谈。',
                ]    
    
    with open("corpus/dictionary_jsyh.json",'r',encoding='utf-8') as json_file:
        dictionary_jsyh=json.load(json_file) 
    
#    org_score = extract_abstract(titles * 1000, contents * 1000, dictionary_jsyh)
#    org_score
    
    lp = LineProfiler()
    lp_wrapper = lp(extract_abstract)
    lp_wrapper(titles * 1000, contents * 1000, dictionary_jsyh)
    lp.print_stats()


#%%
#c = []
#for a in [3,1,4,5,6]:
#    for b in [1,2,3]:
#        if b == a:
#            print(b)
#            c.append(b)
#            break
#    if c:
#        break
    
    
    
