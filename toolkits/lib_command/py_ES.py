# -*- coding: utf-8 -*-
"""
Created on Tue May 22 09:28:14 2018

@author: Administrator
"""



#%%
from datetime import datetime  
from elasticsearch import Elasticsearch  
from elasticsearch import helpers 
from elasticsearch.helpers import bulk  
import pandas as pd
import numpy as np
    
#%% 连接
#es = Elasticsearch(['http://elastic:Wiseweb666@10.19.133.250:5005/'])
es = Elasticsearch(hosts=['127.0.0.1'], port=9200) 
#es_Test = Elasticsearch([{"host":"127.0.0.1","port":9200}])  

# 实例化Elasticsearch类，并设置超时间为120秒，默认是10秒的，如果数据量很大，时间设置更长一些
es = Elasticsearch(timeout=120)
#%% #创建索引
indexName = 'es_db_1'
typeName = 'es_table_1'

# 索引的名字是es_database,如果已经存在了，就返回个400，
# 这个索引可以现在创建，也可以在后面插入数据的时候再临时创建
# create：必须指定待查询的idnex、type、id和查询体body；缺一不可，否则报错 
es.indices.create(index = 'es_db_1')
# {'acknowledged': True, 'shards_acknowledged': True} 
es.indices.refresh(index = indexName)
es.indices.get(index = indexName) # 索引相关信息
# 索引是否存在
if es.indices.exists(index = 'es_db_2'):  # true、false
        es.indices.delete(index = 'es_db_2')  # 删除索引
es.indices.delete(index="test-index", ignore=[400, 404])
#%% 批量索引的命令是bulk，批量索引的提交格式。
j = 0
df = pd.DataFrame(np.arange(1,10001).reshape(100, 100))

count = int(df[0].count())
actions = []
while (j < count):    
    action = {
        "_index": "tickets-index",
        "_type": "tickets",
        "_id": j + 1,
        "_source": {
              "crawaldate":df[0][j],
              "flight":df[1][j],
              "price":float(df[2][j]),
              "discount":float(df[3][j]),
              "date":df[4][j],
              "takeoff":df[5][j],
              "land":df[6][j],
              "source":df[7][j],
              "timestamp": datetime.now()}
        }
    actions.append(action)
    j += 1
 
    if (len(actions) == 500000):
        bulk(es, actions)
        del actions[0:len(actions)]
 
if (len(actions) > 0):
    bulk(es, actions)
    del actions[0:len(actions)]
 
#在这里发现Python API序列化JSON时对数据类型支撑比较有限，原始数据使用的NumPy.Int32必须转换为int才能索引。
#此外，现在的bulk操作默认是每次提交500条数据，我修改为5000甚至50000进行测试，会有索引不成功的情况。
#%% 插入数据,(这里省略插入其他两条数据，后面用)
es.index(index = indexName, doc_type = typeName, id = '01',
         body = {"any":"data01","timestamp":datetime.now()})

#也可以，在插入数据的时候再创建索引test-index
es.index(index = 'es_db_2', doc_type = typeName, id = '02',
         body={"any":"data","timestamp":datetime.now()})

# id并非是一个必选项，如果指定，则该文档的id就是指定值，
# 若不指定，则系统会自动生成一个全局唯一的id赋给该文档。 
body = {"name": 'lucy', 'sex': 'female', 'age': 10} # 新增字段
es.index(index = indexName, doc_type = typeName, id=None, body = body)

#%% 删除数据
# delete：删除指定index、type、id的文档
es.delete(index = 'es_db_2', doc_type = typeName, id = '02') # 索引仍在

# 条件删除 
#　　delete_by_query：删除满足条件的所有数据，查询条件必须符合DLS格式
query = {'query': {'match': {'sex': 'famale'}}}# 删除性别为女性的所有文档
query = {'query': {'range': {'age': {'lt': 11}}}}# 删除年龄小于11的所有文档
es.delete_by_query(index = indexName, doc_type = typeName, 
                   body=query)
#%% 查询数据，两种get and search   
#get获取
# get：获取指定index、type、id所对应的文档
res = es.get(index = indexName, doc_type = typeName, id = '01')
print(res)
print(res['_source'])
 
#search获取
es.search(index='logstash-2015.08.20', 
          q='http_status_code:5* AND server_name:"web1"', 
          from_='124119')
#index - 索引名
#q - 查询指定匹配 使用Lucene查询语法
#from_ - 查询起始点  默认0
#doc_type - 文档类型
#size - 指定查询条数 默认10
#field - 指定字段 逗号分隔
#sort - 排序  字段：asc/desc
#body - 使用Query DSL
#scroll - 滚动查询

# search：查询满足条件的所有文档，没有id属性，且index，type和body均可为None。 
# 搜索，q是指定搜索内容，可以看到空格对q查询结果没有影响，size指定个数，from_指定起始位置，
# q用空格隔开可以多个查询也可以限定返回结果的字段，
# filter_path可以指定需要显示的数据，如本例中显示在最后的结果中的只有_id和_type
res_3 = es.search(index="bank", q="Holmes", size=1, from_=1)
res_4 = es.search(index="bank", q=" 39225    5686 ", size=1000, 
                  filter_path=['hits.hits._id', 'hits.hits._type'])
res_4 = es.search(index="bank", q=" 39225    5686 ", size=1000)

res = es.search(index = indexName, body={"query":{"match_all":{}}})
print(res)
for hit in res['hits']['hits']:
    print(hit["_source"])
    
res = es.search(index = indexName, 
                body={'query':{'match':{'any':'data'}}}) #获取any=data的所有值
print(res) 

# 条件查询
query = {'query': {'match_all': {}}}# 查找所有文档
query = {'query': {'term': {'name': 'jack'}}}# 查找名字叫做jack的所有文档
query = {'query': {'range': {'age': {'gt': 11}}}}# 查找年龄大于11的所有文档
allDoc = es.search(index = indexName, doc_type = typeName, 
                   body=query)
print(allDoc['hits']['hits'][0])# 返回第一个文档的内容

from elasticsearch_dsl import Search
# using参数是指定Elasticsearch实例对象，index指定索引，可以缩小范围，
# index接受一个列表作为多个索引，且也可以用正则表示符合某种规则的索引都可以被索引，
# 如index=["bank", "banner", "country"]又如index=["b*"]后者可以同时索引所有以b开头的索引，
# search中同样可以指定具体doc-type
s = Search(using=es, index="time_appid_placementid_country")
# 根据字段查询，可以多个查询条件叠加,hightlight可以指定高亮，但是我的没有出现高亮，对数据处理没啥用不去深究
res_2 = s.query("match", gender="F").query("match", age="32").highlight("age").execute()
res.to_dict()

# 用Q()对象查询多个对象，在多个字段中，fields是一个列表，可以存放多个field，
# query为所要查询的值，如果要查询多个值可以用空格隔开（似乎查询的时候Q对象只接受同种类型的数据，
# 如果文本和数字混杂在一块就会报错，建立查询语句出错，有待考察，如query="Amber 11"就会失败，
# fields也是一样，另外query可以接受单个数字的查询，如果是多个同样会报相同的错误）

# Q()第一个参数是查询方法，具体用法及其他方法可以参考elasticsearch的官方文档
q = Q("multi_match", query="Amber Hattie", fields=["firstname"])
res_3 = s.query(q).execute()

#%% 过滤
#实例1:范围查询
s = s.filter("range", timestamp={"gte": 0, "lt": time.time()}).query("match", country="in")
#实例2:普通过滤
res_3 = s.filter("terms", balance_num=["39225", "5686"]).execute()

#%% # 聚合，
# 聚合可以放在查询，过滤等操作的后面叠加，需要加aggs，bucket即为分组，
# 其中第一个参数是分组的名字，自己指定即可，第二个参数是方法，
# 第三个是指定的field，metric也是同样，metric的方法有sum、avg、max、min等等，
# 但是需要指出的是有两个方法可以一次性返回这些值，stats和extended_stats，
# 后者还可以返回方差等值，很方便，此过程可能会出现一些错误，具体见本文最后相关bug

# 实例1
s.aggs.bucket("per_country", "terms", field="timestamp").metric("sum_click", "stats", field="click").metric("sum_request", "stats", field="request")

# 实例2
s.aggs.bucket("per_age", "terms", field="click.keyword").metric("sum_click", "stats", field="click")

# 实例3
s.aggs.metric("sum_age", "extended_stats", field="impression")

# 实例4
s.aggs.bucket("per_age", "terms", field="country.keyword")
# 最后依然是要execute，此处注意s.aggs......的操作不能用变量接收（如res=s.aggs......的操作就是错误的），聚合的结果会在res中显示

# 实例5
a = A("range", field="account_number", ranges=[{"to": 10}, {"from": 11, "to": 21}])
# 此聚合是根据区间进行聚合
res = s.execute()
#%% 更新 
# update：跟新指定index、type、id所对应的文档 
body={"any":"data_for_update","timestamp":datetime.now()}
es.update(index = indexName, doc_type = typeName, id = '01', body = body)

#条件更新 
#　　update_by_query：更新满足条件的所有数据，写法同上删除和查询

#%% 批量插入、删除、更新 
#　　bulk：可以同时执行多个操作，单只请求一次，从而在批量操作的时候，可以很大程度上减少程序系统开销。
#  此外，bulk不仅可以一次性批量执行插入、或者删除操作，还可以在一次请求中，既可以插入、又可以删除和更新操作。 
#　　但是需要注意的是，任何一种操作都有固定的文档格式，只有完全符合该格式要求，才可执行成功。
doc = [
     {"index": {}},
     {'name': 'jackaaa', 'age': 2000, 'sex': 'female', 'address': u'北京'},
     {"index": {}},
     {'name': 'jackbbb', 'age': 3000, 'sex': 'male', 'address': u'上海'},
     {"index": {}},
     {'name': 'jackccc', 'age': 4000, 'sex': 'female', 'address': u'广州'},
     {"index": {}},
     {'name': 'jackddd', 'age': 1000, 'sex': 'male', 'address': u'深圳'},
 ]
doc = [
    {'index': {'_index': 'indexName', '_type': 'typeName', '_id': 'idValue'}},
    {'name': 'jack', 'sex': 'male', 'age': 10 },
    {'delete': {'_index': 'indexName', '_type': 'typeName', '_id': 'idValue'}},
    {"create": {'_index' : 'indexName', "_type" : 'typeName', '_id': 'idValue'}},
    {'name': 'lucy', 'sex': 'female', 'age': 20 },
    {'update': {'_index': 'indexName', '_type': 'typeName', '_id': 'idValue'}},
    {'doc': {'age': '100'}},
 ]
es.bulk(index = indexName, doc_type = typeName, body=doc)


#%% 统计
count = es.count(index=indexName)["count"]  #总条数 
es.count(index='logstash-2015.08.21', q='http_status_code:500')
 
#每页多少条  
pageLine = 1000
#多少页  
page = count/pageLine if (count%pageLine) == 0 else count/pageLine+1   
    
#%%
es = Elasticsearch(['http://elastic:Wiseweb666@10.19.133.250:9200/'])
query = {"query":{"match_all":{}}}  
#index = "wiseweb.jxg.annual_initiator_contributive_info" 
index = 'wiseweb.jxg.company_base_business_merge_new' 
resp = es.search(index, body=query)              
es.count(index = index)['count']

#%%
#创建索引   调用create或index方法  
es = Elasticsearch()  
es.create(index="es_database",doc_type="es_table",id=1,  
          body={"any":"data","timesamp":datetime.now()})     #已存在的不可重新创建  
#es.create(index="test",doc_type="test-type",id=1,body={"any":"data","timesamp":datetime.now()})     #已存在的不可重新创建  
#es.indices.delete(index="test-index2",ignore=[400,404])  
   
#%%
from elasticsearch import Elasticsearch  
# 查询索引中的所有内容  

index = "test"  
query = {"query":{"match_all":{}}}  
resp = es.search(index, body=query)  
resp_docs = resp["hits"]["hits"]  
total = resp['hits']['total']  
  
print(total)     #总共查找到的数量  
#print(resp_docs[0]['_source']['@timestamp'])   #输出一个字段  

#%%
es = Elasticsearch(['http://elastic:Wiseweb666@10.19.133.250:9200/'])
query = {"query":{"match_all":{}}}  
#index =  'wiseweb.jxg.company_base_business_merge_new'
indexs = ['wiseweb.jxg.company_base_contact_info',
          "wiseweb.jxg.annual_initiator_contributive_info",
          'wiseweb.jxg.company_base_business_merge',
          'wiseweb.jxg.company_base_business_merge_new']

#resp = es.search(index, body=query)              
#es.count(index = index)['count']

# 所有index的field
columns = {}
for index in indexs:
    es_result = es.search(index, body=query)
    cols = list(es_result['hits']['hits'][0]["_source"].keys())
    columns[index] = [es_result['hits']['total'], cols]
#%%
import time    
def dict_to_dataframe(es_result):
#    es_result = es.search(index, body=query) 
    t0 = time.time()
    values = []
    cols = list(es_result['hits']['hits'][0]["_source"].keys())
    #values.append(cols)
    for result in es_result['hits']['hits']:
        values.append(list(result["_source"].values()))
    values = pd.DataFrame(values, columns = cols)
    t1 = time.time()
    print(t1-t0)
    return values

t0 = time.time()
es_result = es.search(index, body=query, size = 10000) 
t1 = time.time()
print(t1-t0)
values = dict_to_dataframe(es_result)
print(values.shape)
#%%
chuncksize = 100000
t0 = time.time()
ret = helpers.scan(es, query=query, index=index,preserve_order=True)  
t1 = time.time()
print(t1-t0)

t = []
values = []
i = 0
t2 = time.time()
for ind,result in enumerate(ret):    
    cols = list(result["_source"].keys())
    values.append(list(result["_source"].values()))
    if (ind != 0) & (ind%chuncksize == 0):
        i += 1
        t3 = time.time()
        if i > 1:        
            print('-- 第 %s 次循环结束，费时：', t3-t4)        
        print('-- 第 %s 次，编号：'%i, ind)
        values = pd.DataFrame(values, columns = cols)
        print('values.shape', values.shape)
        print(values.head())
        values = []
        t4 = time.time()
        if i == 1: print('-- 第 %s 次循环结束，费时：'%i, t4-t2)
        
    
t5 = time.time()
print('-- 循环结束，共 %s 次，共费时：'%i, t5-t2)        
        
    


#%%

