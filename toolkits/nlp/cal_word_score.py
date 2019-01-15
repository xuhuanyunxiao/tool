#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import jieba
from toolkits.nlp import utils

dir_path = os.path.dirname(os.path.abspath(__file__))
# 加载其他自定义词典
jieba.load_userdict(os.path.normpath(dir_path + '/corpus/insurance_dict_20180803.txt'))
jieba.load_userdict(os.path.normpath(dir_path + '/corpus/bank_dict_20180814.txt'))

#%%
def extract_abstracts(titles, contents, dictionarys):
    pos_flag = 'jsyh'
    utils.load_entity_dict(dictionarys, pos_flag)
    org_score = []
    for title, content in zip(titles, contents):
        org_score_list, vip_word, key_sentence, purity = utils.extract_abstract(title, 
                                                                                 content, 
                                                                                 dictionarys, 
                                                                                 pos_flag)
        org_score.append([org_score_list, [vip_word, key_sentence], purity])
    
    utils.del_entity_dict(dictionarys, pos_flag)
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
    lp_wrapper = lp(utils.extract_abstract)
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
    
    
    
