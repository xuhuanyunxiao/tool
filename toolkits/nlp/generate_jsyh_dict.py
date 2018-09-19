#!/usr/bin/env python
# -*- coding: utf-8 -*-


from toolkits.setup.specific_func import get_engine
import pandas as pd
import json

#%% mysql
engine = get_engine('cbirc')

#%%
sql_sel = '''
SELECT 
    t1.id, t2.name, t1.classify_id, t1.subject_word
FROM
    cbrc_circ.db_class_tree_node_keyword t1
        LEFT JOIN
    cbrc_circ.db_class_tree_node t2 ON t1.node_id = t2.id
WHERE
    t1.flag = 0 AND t1.type != 4
        AND classify_id IN (1 , 2, 3, 4, 5, 6, 21);
                '''

node_keyword_1 = pd.read_sql(sql_sel,engine)
node_keyword_1['level'] = node_keyword_1.apply(lambda x:'second_level' if x['classify_id'] == 3 else 'third_level', axis = 1)

#%% excel
node_keyword_2 = pd.read_excel('jsyh_beijing_name.xlsx')

node_keyword_2['name'] = node_keyword_2['全称']
node_keyword_2['subject_word'] = node_keyword_2['关键词']
node_keyword_2['level'] = 'first_level'

#%%
node_keyword_3 = pd.read_excel('bank_org.xlsx')

node_keyword_3['name'] = node_keyword_3['银行名称']
node_keyword_3['subject_word'] = node_keyword_3['银行同义词']
node_keyword_3['level'] = 'first_level'

#%%
node_keyword = pd.concat([node_keyword_1[['name', 'subject_word', 'level']], 
                          node_keyword_2[['name', 'subject_word', 'level']], 
                          node_keyword_3[['name', 'subject_word', 'level']]])

node_keyword['index'] = range(node_keyword.shape[0])
node_keyword = node_keyword.set_index('index')
node_keyword = node_keyword.fillna('')
print(node_keyword.describe())
node_keyword = node_keyword.fillna('')
print(node_keyword.describe())

#%%
node_keywordss = node_keyword[~node_keyword['name'].isin(['国有商业银行', '股份制商业银行', '民营银行', 
                '政策性银行', '资产管理公司', '其他金融机构', '互联网金融'])]
#node_keywordss[['name', 'subject_word']].to_excel('词表_20180914.xlsx', index = False)

#%% dict and json
dictionary_jsyh = {}
#for index in node_keyword.index:
#    name = node_keyword['name'][index]
#    level = node_keyword['level'][index]
#    subject_word = node_keyword['subject_word'][index]
#    
#    word_list = subject_word.split(' ')
#    word_list.append(name)
#
#    for word in word_list:
#        if len(word) > 1:
#            if level not in dictionary_jsyh:
#                dictionary_jsyh[level] = {}
#            else :
#                dictionary_jsyh[level][word] = name


for index in node_keyword.index:
    name = node_keyword['name'][index]
    if name in ['国有商业银行', '股份制商业银行', '民营银行', 
                '政策性银行', '资产管理公司', '其他金融机构']: 
        continue
    level = node_keyword['level'][index]
    subject_word = node_keyword['subject_word'][index]
    
    word_list = str(subject_word).split(' ')
    word_list.append(name)

    for word in word_list:
        if word in ['国元信托','建信信托']:
            print(index, word, name)
        if len(word) > 1:
            if word not in dictionary_jsyh:
                dictionary_jsyh[word] = name
            else :
                if name != dictionary_jsyh[word]:
                    pass
#                    print(index, word, name, dictionary_jsyh[word])
            if len(word) <3 :
                print(word, dictionary_jsyh[word])
#%%
with open("./dictionary_jsyh.json",'w',encoding='utf-8') as json_file:
    json.dump(dictionary_jsyh,json_file,ensure_ascii=False)

#%%
#model={} #存放读取的数据
#with open("./dictionary_jsyh.json",'r',encoding='utf-8') as json_file:
#    model=json.load(json_file)




