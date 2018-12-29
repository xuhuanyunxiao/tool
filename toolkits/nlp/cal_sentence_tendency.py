#!/usr/bin/env python
# -*- coding: utf-8 -*-
import jieba
from toolkits.nlp import utils
from toolkits.nlp import utils_tendency
import os

dir_path = os.path.dirname(os.path.abspath(__file__))
# 加载自定义词典
jieba.load_userdict(os.path.normpath(dir_path + r"/corpus/insurance_dict_20180803.txt"))
jieba.load_userdict(os.path.normpath(dir_path + r"/corpus/bank_dict_20180814.txt"))

sentiment_emotion_dict, sentiment_privative_dict, \
    sentiment_transitional_dict, sentiment_degree_dict = utils_tendency.load_sentiment_dict()
# utils_tendency.del_sentiment_dict()

#%%
# mysql 加载实体词典
def load_mysql_dict(dictionarys): 
    for assist_worda in dictionarys['assistA_word_list']:
	     jieba.add_word(assist_worda, 100, "assist_a")
    for assist_wordb in dictionarys['assistB_word_list']:
	     jieba.add_word(assist_wordb, 100, "assist_b")
    for remove_word in dictionarys['remove_word_list']:
	     jieba.add_word(remove_word, 100, "rm")
    for subject_word in dictionarys['subject_word_list']:
	     jieba.add_word(subject_word, 100, "cpn")
         
def del_mysql_dict(dictionarys): 
    for assist_worda in dictionarys['assistA_word_list']:
        try :        
            jieba.del_word(assist_worda)
        except :
            continue            
    for assist_wordb in dictionarys['assistB_word_list']:
        try :        
    	     jieba.add_word(assist_wordb)
        except :
            continue             
    for remove_word in dictionarys['remove_word_list']:
        try :        
    	     jieba.del_word(remove_word)       
        except :
            continue     
    for subject_word in dictionarys['subject_word_list']:
        try :
            jieba.del_word(subject_word)
        except :
            continue

#%%
def evaluate_article(classify_id_list, title, content, dictionarys):
    '''
    计算一篇文章倾向、以及每个主体的倾向
    '''
    
#    load_mysql_dict(dictionarys)
    # title
    pre_titles = utils_tendency.preprocess_sentences([title])
    pre_title = pre_titles[0]
    title_score, title_rule_index = utils_tendency.cal_sen_tend(0, pre_title)
    
    title_pos_word = []
    for pos,word in zip(pre_title[0], pre_title[1]):
        if pos in ['emotion', 'privative', 'transitional', 'degree']:
            if pos == 'emotion':
                weight = sentiment_emotion_dict[word]
            elif pos == 'degree':
                weight = sentiment_degree_dict[word]  
            elif pos == 'privative':
                weight = 0.8 
            elif pos == 'transitional':
                weight = 1.2                  
            title_pos_word.append((pos, word, weight))
    
    # content
    content = utils.clear_sen(str(content))  # clear_article
    sentences = [i.strip() for i in utils.cut_sentences(content)]
    pre_sentences = utils_tendency.preprocess_sentences(sentences)    
    
    content_score = 0
    org_score_list = []
    org_sentences_pos_word_weight = []
    if len(pre_sentences) > 0:
        org_list, org_loc, aka_name_dict = utils_tendency.get_entity_new(pre_sentences, sentences, dictionarys)                    
        org_score_dict, org_sen_loc, \
        org_sentences_pos_word_weight = utils_tendency.cal_sentences_tendency_new(pre_sentences, 
                                                               org_loc, sentences)    

        for cpn in org_list:
            # 选出 保险机构 用于判断倾向性 （classify_id)
#            保监会用于判断倾向的classify_id：6
#            中国人寿用于判断倾向的classify_id：21、27、29
#            if cpn['classify_id'] in classify_id_list:
            if cpn['classify_id'] in [6, 21, 27, 29]:
                try :
                    cpn['org_tendency_score'] = org_score_dict[cpn['name']]
                except:
                    cpn['org_tendency_score'] = org_score_dict[cpn['aka_name']]
                    
                content_score += cpn['org_tendency_score']
                
            else :
                cpn['org_tendency_score'] = 0 # 未选择的机构都为非负  
                
            # 转换成两类
            if cpn['org_tendency_score'] < 0:
                cpn['org_tendency_score'] = -1
            else:
                cpn['org_tendency_score'] = 0 
                
            org_score_list.append(cpn)     

    chapter_tendency_score = title_score * 0.6 + content_score * 0.4
    
    # 转换成两类
    if chapter_tendency_score < 0:
        chapter_tendency_score = -1
    else:
        chapter_tendency_score = 0
        
#    del_mysql_dict(dictionarys)

    return chapter_tendency_score, org_score_list
#    return chapter_tendency_score, org_score_list, title_score, content_score, title_rule_index, title_pos_word, org_sentences_pos_word_weight

def process_articles(types, titles, contents, dictionarys):
    load_mysql_dict(dictionarys)
    
    types = str(types)
    if types == '1':
        classify_id_list = []
    elif types == '2':
        classify_id_list = []
    elif types == '3':
        classify_id_list = []  
    elif types == '4':
        classify_id_list = []
    elif types == '5':
        classify_id_list = []         
    else :
        raise Exception("Invalid types!",'there is no types.')
    
    org_res = []
    chapter_res = []
    for title, content in zip(titles, contents):
        chapter_tendency_score, org_score_list = evaluate_article(classify_id_list, title, content, dictionarys)
        chapter_res.append(chapter_tendency_score)
        org_res.append(org_score_list)
        
    del_mysql_dict(dictionarys)
    return chapter_res, org_res

#%%
if __name__ == '__main__':
    import json
    from line_profiler import LineProfiler
    
    dictionarys = dictionarys_3
    
    titles = ['监管部门拟调研P2P平台保证人保资管的保险业务避免陷入混乱',
              '不只是江苏，黑龙江、安徽、河南等多地税务机关开始追缴社保费']
    contents = ['''保监会北京监管局将要重拳打击证券行业的的乱象。
                他们会进一步考虑引入其他机制。
                那样，北京保监局就难以在短期内有所动作。
                不知道这对汇丰人寿是不是一个好消息？
                证券市场也许就会有更规范的秩序，保证交易合理有序进行。
                这样的现象也正在影响其他城市，未曾开始的领域还有很多！
                当然，现在仍有许多专业人士就这些吵的不可开交。
                但是，至于有多少用处就不知道了，国寿公司也在配合监管部门。
                总之， 保险监督管理委员会上海监管局也在强化监管层面的政策。''',
                '平安集团 马明哲董事长 保险 银行 普惠 好房 好医生 30年历史 6.5万亿资产 世界500强第29位 金融领域全球排名第6位。 ',
                '中国人寿开封分公司总经理张敬明、中国人寿财险中心支公司总经理江河军作为市政协委员参加开封市第十二届一次会议。',
                '节奏紧凑，场面火爆[亲亲]@小娜侬她娘的女儿 @一米养光 @广东汕头中国人寿莫结飞',
                '这是八百里伏牛山之精髓 远游天高云闲，近听雀鸟嘶鸣 空谷溪响，群瀑贯穿 山高水长绿荫夹道而生，豁然开朗间 良田层叠，屋舍淡然 这里因山路崎岖受到户外驴友的关注 这里是徒步野游的小众地点 闲云野鹤，妙趣横生 因地处伏牛山深处 当河南大部分地区枝繁叶茂 这里的秋色已经渐渐铺开 一层一层 从山间谷底到田间山头 秋色一步步将这里霸占 这里直到今年年初才通公路，这里的美才能被更多人发现 旅行亮点 Travel Lightspot 这是一次和大自然亲密融合的旅程 沟内树木茂密，参天大树相映成辉 青藤树蔓缠绕其间，层绿叠嶂 放眼望去颇有原始森林的感觉 走在山间林木下 溪水在脚边簌簌而过 清风拂面，树影斑驳 一不留心便惊起了一从飞鸟 这不仅仅是徒步，更是一次深山探秘 不仅仅要看美景，我们追求的是探寻 没有缆车没有景交车，一路徒步前往 不设路线，随心所遇，你见到的都是独一份 除却这些，你还能收获一次山水田园的记忆 城市的车水马龙带给我们的是匆忙疲惫 这一次返璞归真，归隐山野可好 简朴的青瓦黄土墙，是来自北方乡村遥远的影像 在这里，一帧一画历历在目 走近那段自给自足的岁月，春耕种、秋收获 感受最淳朴自然的山野情节 领队：中国登山协会山地户外指导员； 保险：30万保额旅游意外险； 公装：紧急救助药品等。 住宿：一晚大山深处农家客栈',
                '点击蓝字 关注我们 2018年度中国人保财产青海分公司“千人工程”招聘项目        2018年度中国人保财产青海分公司“千人工程”招聘项目公告已于9月30日在中国人保财产官网发布，海南州国企招聘考试网整理发布本次招聘报名简历投递时间：10月8日-10月30日，请需要的考生及时查看：        中国人民财产保险股份有限公司青海省分公司因业务发展需要现面向社会招聘保险销售类人才，殷切希望有志之士加入我们! 方法一：（扫文末二维码进公告原文查看详情） 备注：如果打不来链接的小伙伴们请按照方法二查看招聘职位详情 方法二：（扫文末二维码进公告原文查看详情） 公告附件 长按识别二维码查看 点击阅读原文查看近期国企招聘信息汇总！']
#    process_articles(titles, contents, dictionarys)
    
#    
    title = contents[1]
    content = contents[2]
#    
#    with open("corpus/dictionary_jsyh.json",'r',encoding='utf-8') as json_file:
#        dictionary_jsyh=json.load(json_file) 
#    
#    org_score = extract_abstract(titles * 1000, contents * 1000, dictionary_jsyh)
#    org_score
#    
#    lp = LineProfiler()
#    lp_wrapper = lp(extract_abstract)
#    lp_wrapper(titles * 1000, contents * 1000, dictionary_jsyh)
#    lp.print_stats()


#%%
#import pandas as pd
#
#data = pd.read_excel('circ_class_predict_mysql_2018-10-07.xlsx')
#data = data.iloc[:300, :]
#titles = data['title'].tolist()
#contents = data['content'].tolist()
##chapter_res, org_res = process_articles(titles, contents, dictionarys)
#
##%%
#org_res = []
#chapter_res = []
#index = -1
#for title, content in zip(titles, contents):
#    try :
#        index += 1
#        
#        id = data.loc[index, 'id']
#        predict_label = data.loc[index, 'predict_label']
#        chapter_tendency_score, org_score_list, title_score, content_score, title_rule_index, title_pos_word = evaluate_article(title, content, dictionarys)
#        chapter_res.append([id, predict_label, title,content, chapter_tendency_score, title_score, content_score, title_rule_index, str(title_pos_word), str(org_score_list)])
#        org_res.append(org_score_list)
#        
#    except Exception as e:
#        print(index)
#        print(e)
#        continue
#    
#ss = 'id,predict_label,title,content,chapter_tendency_score,title_score,content_score,title_rule_index,title_pos_word,org_score_list'
#chapter_res = pd.DataFrame(chapter_res, columns = ss.split(','))
#chapter_res.to_excel('circ_chapter_tendency_score_300.xlsx', index = False)

#%%









