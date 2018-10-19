#!/usr/bin/env python
# -*- coding: utf-8 -*-
#%%
#import pymysql
import logging.config
import time

from sqlalchemy import create_engine
from pandas.io import sql
import pandas as pd

#%%
# 日志记录
logging.config.fileConfig("conf/logger.conf")
logger = logging.getLogger("rotating")

#%%
def get_dicts(types = '2'):
    """
    获得自定义词典
    :return:
    """
    start_timestamp = time.time()
    logger.info("starting get_dicts...")      

    try:
        DB_CON_STR = 'mysql+pymysql://wisedb:Wi$eWeb321@10.31.149.216:5720/cbrc_circ?charset=utf8' 
        engine = create_engine(DB_CON_STR, echo=False)
        cur = sql.execute('show databases', engine)
    except :
        DB_CON_STR = 'mysql+pymysql://wisedb:Wi$eWeb321@39.107.203.231:5720/cbrc_circ?charset=utf8'  
        engine = create_engine(DB_CON_STR, echo=False)
        cur = sql.execute('show databases', engine)

    sql_node = "select id, name from db_class_tree_node where flag = 0"
    node_name = pd.read_sql(sql_node, engine)
    
    node_name_dict = {key:value for [key, value] in node_name.values}

    # SQL 查询语句, 内容只取第一段内容
    sql_c = """
    select id, name, subject_word, assist_worda, assist_wordb, 
        remove_word, classify_id, node_id 
        from db_class_tree_node_keyword 
            where type in (0, {0}) and flag = 0
    """.format(types)

    try:        
        cur = sql.execute(sql_c, engine)  # 执行SQL语句
       
        data = {}
        subject_word_dict = {}
        assistA_word_list = []
        assistB_word_list = []
        remove_word_list = []
        # 获取所有记录列表
        for row in cur.fetchall():
            # print(row)
            word_id = row[0]
            
            subject_word = row[2].strip()  # 主体词（标准名称的检测）
            assist_worda = row[3].strip()  # 辅助词A
            assist_wordb = row[4].strip()  # 辅助词B
            remove_word = row[5].strip()  # 去除词（如果包含，则该句不做判别）
            classify_id = row[6]
            node_id = row[7]
            
            try :
                name = node_name_dict[node_id]
            except :
#                print(row)
                name = str(row[1]).strip()  # 标准名称（用于最终返回）
            
            
            if (name != '') & (name not in ['None', 'none','nan', 'NaN']):  # 标准名称
                if name not in subject_word_dict.keys():                        
                    subject_word_dict[name] = [word_id] 
                else :
                    if word_id not in subject_word_dict[name]:
                        subject_word_dict[name].append(word_id)
            if subject_word != '':
                for sub_name in subject_word.split(' '):  # 主体词
                    sub_name = sub_name.strip()
                    if sub_name != '':
                        if sub_name not in subject_word_dict.keys(): 
                            subject_word_dict[sub_name] = [word_id] 
                        else :
                            if word_id not in subject_word_dict[sub_name]:
                                subject_word_dict[sub_name].append(word_id)
            if assist_worda != '':
                assistA_word_list.extend(assist_worda.split(' '))  # 辅助词A
            if assist_wordb != '':
                assistB_word_list.extend(assist_wordb.split(' '))  # 辅助词B                                
            if remove_word != '':
                remove_word_list.extend(remove_word.split(' '))  # 去除词
            
            data[word_id] = (word_id, classify_id, node_id, name, 
                            subject_word, assist_worda, 
                            assist_wordb, remove_word)
        dictionarys = {'data':data,
                       'subject_word_list':subject_word_dict,
                       'assistA_word_list':list(set(assistA_word_list)), 
                       'assistB_word_list':list(set(assistB_word_list)), 
                       'remove_word_list':list(set(remove_word_list))}
        logger.info("ending get_dicts, {cost_times: %ds}" % (time.time() - start_timestamp))
    except Exception as e:
        print(e)
        logger.error("Error: get_dicts, {exception: %s}" % e)
    finally:        
        engine.dispose()  # 关闭数据库连接
        return dictionarys
#%%

if __name__ == '__main__':
#    print(get_dicts())

    dictionarys = get_dicts()
#    for dictionary in dictionarys:
#        print(dictionary)

#    print(dictionarys['北京保监局'])