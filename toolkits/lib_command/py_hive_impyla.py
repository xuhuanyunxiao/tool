# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 11:29:05 2018

@author: Administrator
"""


#%%
from impala.dbapi import connect
from impala.util import as_pandas

############  impala.dbapi.connect.curosr  ##########
##### close  database_exists  description  execute  fetchall  fetchone
##### fetchmany  database_exists  table_exists  get_databases  get_tables
##### get_table_schema status

#需要注意的是这里的auth_mechanism必须有，但database不必须
conn = connect(host="192.168.20.102", port=10000,  # database="system", 
               auth_mechanism="PLAIN",
               user = 'admin', password = 'admin')
cursor = conn.cursor()

# 查看基础信息
cursor.execute("show databases")
database_name_list = cursor.fetchall()
cursor.execute('use system')
#cursor.execute('SHOW Tables')
#print(cursor.fetchall())
#print(cursor.description) # prints the result set's schema
#cursor.database_exists('system')
# cursor.table_exists('company_base_business')
# cursor.get_databases();results = cursor.fetchall()
# cursor.get_tables();results = cursor.fetchall()
# results =cursor.get_table_schema('company_base_business')
# cursor.status()
#

# 获取数据
cursor.execute("select * from company_base_business")
## results = cursor.fetchall()
df = as_pandas(cursor)
#
df_1 = df.iloc[:5,:]

# 写入数据
database_name = 'my_data'
table_name = 'my_table'

def run_hive_query(sql):   
    cursor.execute(sql)  
    return cursor.fetchall() 
   
database_list = [name[0] for name in run_hive_query("show databases")]
if database_name not in database_list:  
    with conn.cursor() as cursor:  
        cursor.execute("create database " + database_name) 
        
cursor.execute("use "+ database_name) 
    
table_list = [name[0] for name in run_hive_query("show tables")] 
if table_name not in table_list:  
    cursor.execute("create table %s like system.company_base_business"%table_name)
    
else:  
    pass

cursor.close()

#
#col_list = tuple(df.columns.tolist())
#cursor.execute("insert into table my_table values{0}".format(tuple(df.iloc[1,:].tolist())))
#cursor.execute("insert into my_table select  * from system.company_base_business")
#cursor.execute("drop table my_table")

#cursor.execute('use data_hub_new')
#sql_command = 'create table buse_business_test like data_hub.buse_business_test'
#cursor.execute(sql_command)
#sql_command = 'select * from data_hub.buse_business_test'
#cursor.execute(sql_command)

#%%
# merge (n1:Company {name:'国开发展基金有限公司',state:'开业', regis_cap:'5000000',legal_name:'王用生'})

database_name = 'etl_data'
cursor.execute("use "+ database_name) 

table_name = 'company_base_business_merge_new'
cursor.execute("select * from %s"%table_name)
business = as_pandas(cursor)
#business = business.drop([0], axis = 0)
#business = business.iloc[:5,:]
#%%
#save_filename = result_folder + '\\图谱语句_match_' + today + '.txt' 
save_filename = result_folder + '\\图谱语句_merge_' + today + '.txt' 
file = open(save_filename,"w")
for index in business.index:
    names = business['company_name'][index]
    state = business['company_operat_state'][index]
    regis_cap = business['company_regis_capital'][index]
    legal_name = business['company_legal_name'][index]
#    file.write("match (n_%s:Company{name:'%s'}),(b_%s:Person{name:'%s'}) Merge(b_%s)-[:法人]->(n_%s)"\
#               %(index, names, index+1, legal_name, index +1, index) + "\n")  
    file.write("merge (n%s:Company {name:'%s',state:'%s', regis_cap:'%s',legal_name:'%s'})"\
               %(index,names,state,regis_cap,legal_name) + "\n")       
file.close()

#%%
for index in business.index:
    names = business['company_name'][index]
    state = business['company_operat_state'][index]
    regis_cap = business['company_regis_capital'][index]
    legal_name = business['company_legal_name'][index]  
    print("match (n_%s:Company{name:'%s'}),(b_%s:Person{name:'%s'}) Merge(b_%s)-[:法人]->(n_%s)"%(index, names, index+1, legal_name, index +1, index))
#    print("merge (n%s:Company {name:'%s',state:'%s', regis_cap:'%s',legal_name:'%s})'" %(index,names,state,regis_cap,legal_name))
     

