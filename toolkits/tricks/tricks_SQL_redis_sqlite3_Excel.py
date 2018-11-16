
#%% -----------------     Excel  ----------------------
with pd.ExcelWriter(data_folder + '\\try_data.xlsx') as writer:
    pd.DataFrame(try_data).to_excel(writer)
    writer.save() 

import xlrd
from xlutils.copy import copy as xl_copy
from win32com.client import Dispatch

excel = xlrd.open_workbook(currentPath)
sheet_names = [sheet.name for sheet in excel.sheets()]


def write_null(filename):     
    '''
    有些Excel文件必须先打开，修改点什么，例如增加一个空表，才能被读取。
    增加一个空表，但只能针对扩展名为 .xls 的文件
    '''    
    xlApp = Dispatch('Excel.Application')
    xlApp.Visible = False
    xlApp.Workbooks.Open(filename) 
    sheet_name = [i.Name for i in xlApp.Worksheets]
    xlApp.Quit() 
    if 'null_value' not in sheet_name:  
        xlApp = Dispatch('Excel.Application')
        xlApp.Visible = False
        xlApp.Workbooks.Open(filename) 
        xlApp.Worksheets.Add().Name = 'null_value'
        xlApp.ActiveWorkbook.Save()
        xlApp.Quit() 

#%% -----------------     sqlite3  ----------------------
# 内存数据库
import sqlite3

# 连接内存数据库
conn = sqlite3.connect('corpus/circ_signatures_memory.db')
cur = conn.cursor()

# 是否存在表，存在则删除
sql_drop = 'drop table if exists wise_web_signatures_memory'
cur.execute(sql_drop)

# 是否存在表，不存在则创建
sql_create = 'create table if not exists wise_web_signatures_memory ( \
                    id INTEGER PRIMARY KEY, \
                    publishtime VARCHAR(12), \
                    signatures VARCHAR(1000))'
cur.execute(sql_create)

# 在SQLite 并没有 truncate table命令，但可以使用SQLite的delete命令删除现有的表的完整数据，
# 但建议使用DROP TABLE命令删除整个表，并重新创建一遍。
DELETE FROM table_name;
DROP TABLE table_name;

# 读取 mysql
sql_sel = 'select * from {0}'.format(table_name)
mysql_cur.execute(sql_sel)
table_data = mysql_cur.fetchall()
logger.infor("process mysql table: %s, num:%s"%(table_name, len(table_data)))

# 写入内存数据库
sql_sel = 'select count(id) from {0}'.format(table_name)                    
sel_num = memory_cur.execute(sql_sel).fetchall()

sql_truncate = 'delete from {0}'.format(table_name)
memory_cur.execute(sql_truncate)
memory_conn.commit()
sel_num = memory_cur.execute(sql_sel).fetchall()

# 内存数据库：批量
insert_memory_sql = "INSERT INTO {0} VALUES (?, ?, ?);".format(table_name)
memory_cur.executemany(insert_memory_sql, table_data) # 批量插入
memory_conn.commit()
sel_num = memory_cur.execute(sql_sel).fetchall()

# 内存数据库：单条
insert_memory_sql = "INSERT INTO {0} VALUES (?, ?, ?)".format(table_name)
memory_cur.execute(insert_memory_sql, [repeated_id_max, publishtime_max, sig])
memory_conn.commit()

# mysql：单条
sql_mysql_insert = "insert into {0} (id, publishtime, signatures) VALUES (%s,%s,%s)".format(table_name)
mysql_cur.execute(sql_mysql_insert, [repeated_id_max, publishtime_max, sig])
mysql_conn.commit() 


#%% -----------------     MySQL  ----------------------
import pymysql
db = pymysql.connect(host='47.95.148.133', user='wisedb', passwd='Wi$eWeb123', 
                             db='pom', charset='utf8', port=5718) 

cursor = db.cursor()
cursor.execute('show tables')
cursor.fetchall()

#
from toolkits.setup import specific_func 
engine = specific_func.get_engine('circ')

# ----------------------------------
from sqlalchemy import create_engine
from pandas.io import sql

DB_CON_STR = 'mysql+pymysql://root:123456@localhost/mysql_data?charset=utf8'  
engine = create_engine(DB_CON_STR, echo=False) 

sql.to_sql(questionnarie_data, 'try_data', engine, schema='mysql_data', if_exists='replace') 

# create engine
DB_CON_STR = 'mysql+pymysql://root:123456@localhost/mysql_data?charset=utf8'  
engine = create_engine(DB_CON_STR, echo=False) #True will turn on the logging  
# echo标识用于设置通过python标准日志模块完成的SQLAlchemy日志系统，
# 当开启日志功能，我们将能看到所有的SQL生成代码

# read data form mysql
# data_1 = pd.io.sql.read_sql_table('mysql_mtcars',engine)
table_data = pd.read_sql('mysql_mtcars', engine) # 返回DataFrame

# 表操作    
## 显示已有表名
#pd.read_sql_query('show tables', engine)
#pd.read_sql_query('desc mysql_mtcars', engine)
sql.execute('show tables', engine).fetchall()
sql.execute('desc mysql_mtcars', engine).fetchall()

## 删除表
#pd.read_sql_query('drop table if exists tablename', engine) # 如果表存在则删除
sql.execute('drop table if exists tablename', engine)

## 创建表
sql_cmd = """CREATE TABLE EMPLOYEE (
         FIRST_NAME  CHAR(20) NOT NULL,
         LAST_NAME  CHAR(20),
         AGE INT,  
         SEX CHAR(1),
         INCOME FLOAT )"""
sql.execute(sql_cmd, engine)

# 表内容操作   ----------------- 
## 查询/获取
sql_cmd = "SELECT * FROM mysql_mtcars WHERE am = '%d'" % (1)
select_data = pd.read_sql(sql_cmd, engine) # 返回DataFrame

## 根据多个ID查询数据




# write data to mysql
#pd.io.sql.to_sql(data,'tablename', engine, schema='mysql_data', if_exists='replace') 
table_data.to_sql('tablename', engine, schema='mysql_data', if_exists='replace') 


# 关闭连接   ----------------- 
conn = create_engine('mysql+pymysql:user:passwd@host:port/db?charset=etf-8')
try:
    with con:
            dataIn2File.to_sql(table_name,con=conn,if_exists='append',index=False)
except Exception as ee:
    logger.error("fileToMysql fialed",ee)
    traceback.print_exc()
finally:
    conn.dispose()


# pandas 读取 mysql 速度慢  -----------------------
# 原生方法
# 100万数据，在oracle数据库中，使用最方便的pandas自带的read_sql方法
# 代码是方便了，不过用了快10分钟，dataframe才初始化完成
import pandas as pd
import sqlalchemy as sql
db_engine=sql.create_engine('oracle://test01:test01@test001db')
db_df1=pd.read_sql('select * from my_table1',db_engine)

# 通过JDBC查询的方式
# 多几行代码，不过2分钟就完成了dataframe的初始化动作
import pandas as pd
import sqlalchemy as sql
db_engine=sql.create_engine('oracle://test01:test01@test001db')
conn=ora_engine.raw_connection()
cursor=conn.cursor()
queryset=cursor.execute('select * from my_table1')
columns=[for i[0] in queryset.description]
jdbc_data=queryset.fetchall()
db_df1=pd.DataFrame(
jdbc_data,columns=["A1","B2","C3"])
db_df1.columns=columns
db_df1.append(df_data)


import cStringIO
 
output = cStringIO.StringIO()
# ignore the index
df_a.to_csv(output, sep='\t',index = False, header = False)
output.getvalue()
# jump to start of stream
output.seek(0)
 
connection = engine.raw_connection() #engine 是 from sqlalchemy import create_engine
cursor = connection.cursor()
# null value become ''
cursor.copy_from(output,table_name,null='')
connection.commit()
cursor.close()

# 本来50万条数据，使用pd.to_sql方法，设置chunksize=2000，跑了5个小时。
# 而上面这个方法，插40万条数据，只需1分钟。
# 其实原理是使用了pg内置的copy_from方法，SUPER FAST！


id_list = tuple(day_id_1['id'].tolist())

#  ----------------- 
# 保监会
try :
    DB_CON_STR = 'mysql+pymysql://wisedb:Wi$eWeb123@10.80.88.73:5718/pom?charset=utf8'  
    engine = create_engine(DB_CON_STR, echo=False) 
    sql.execute('show databases', engine)
except :
    DB_CON_STR = 'mysql+pymysql://wisedb:Wi$eWeb123@47.95.148.133:5718/pom?charset=utf8'  
    engine = create_engine(DB_CON_STR, echo=False) 
    sql.execute('show databases', engine)    

# 银监会
try :
    DB_CON_STR = 'mysql+pymysql://atlas:WiseWeb123@47.93.77.228:5636/pom?charset=utf8'  
    engine = create_engine(DB_CON_STR, echo=False) 
    sql.execute('show databases', engine)
except :
    DB_CON_STR = 'mysql+pymysql://atlas:WiseWeb123@10.28.205.96:5636/pom?charset=utf8'  
    engine = create_engine(DB_CON_STR, echo=False) 
    sql.execute('show databases', engine)    

# 银保监会、人寿、建行
try:
    DB_CON_STR = 'mysql+pymysql://wisedb:Wi$eWeb321@10.31.149.216:5720/cbrc_circ?charset=utf8' 
    engine = create_engine(DB_CON_STR, echo=False)
    cur = sql.execute('show databases', engine)
except :
    DB_CON_STR = 'mysql+pymysql://wisedb:Wi$eWeb321@39.107.203.231:5720/cbrc_circ?charset=utf8'  
    engine = create_engine(DB_CON_STR, echo=False)
    cur = sql.execute('show databases', engine)   


#%% -----------------     Hive SQL  ----------------------
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

#
#col_list = tuple(df.columns.tolist())
#cursor.execute("insert into table my_table values{0}".format(tuple(df.iloc[1,:].tolist())))
#cursor.execute("insert into my_table select  * from system.company_base_business")
#cursor.execute("drop table my_table")

cursor.close()


#%% -----------------     Hive to MySQL  ----------------------
#%% 全量  Hive to MySQL
from impala.dbapi import connect
from impala.util import as_pandas

from sqlalchemy import create_engine
from pandas.io import sql
import pandas as pd

# MySQL
DB_CON_STR = 'mysql+pymysql://root:123456@localhost/data_analysis?charset=utf8'  
engine = create_engine(DB_CON_STR, echo=False) 

# Hive
conn = connect(host="192.168.20.102", port=10000,  # database="system", 
               auth_mechanism="PLAIN",
               user = 'admin', password = 'admin')
cursor = conn.cursor()
def run_hive_query(sql_command):   
    cursor.execute(sql_command)  
    return cursor.fetchall() 

database_name = 'data_analysis'
cursor.execute("use "+ database_name) 

table_list = [name[0] for name in run_hive_query("show tables")] 

for table_name in table_list:
    cursor.execute("select * from %s"%table_name)
    tmp_data = as_pandas(cursor)
    sql.to_sql(tmp_data, table_name, 
           engine, schema='data_analysis', if_exists='replace') 

#%% 循环读取数据 ----------------------------
chunksize = 100000

for index, table_name in enumerate(table_list[:2]):
    print('-- 处理第 %s 张表：%s'%(str(index+1), table_name))
    
    # mysql 存在表则删除
    sql.execute('drop table if exists %s'%table_name, engine)
    
    # hive 获取数据    
    cursor.execute("select count(*) from %s"%table_name)
    lines = cursor.fetchall()
    loop = int(lines[0][0] / chunksize) + 1 
    print(' ****  ', loop)
    # loop = 3
    
    cursor.execute("select * from %s"%table_name)
    
    for i in range(loop):
        print('  ---- 共 %s 次循环，第 %s 次循环'%(str(loop), str(i+1)))
        if i == 0: # 设置表头
            tmp_data = cursor.fetchmany(chunksize)
            fields = tmp_data[0]
            tmp_data = pd.DataFrame(tmp_data, columns = fields) 
        else :
            tmp_data = cursor.fetchmany(chunksize)
            tmp_data = pd.DataFrame(tmp_data, columns = fields)             
        print(tmp_data)           
        sql.to_sql(tmp_data, table_name, engine, 
                   schema='data_analysis', if_exists='append')   

save_filename = os.path.join(result_folder, 'hadoop_put_data.txt')
file = open(save_filename,"w")



# 读取csv文件几行数据，在hive上建立外联表，同时写hadoop上的关联语句
database_name = 'data_analysis'
cursor.execute("create database if not exists {0} ".format(database_name))
cursor.execute("use "+ database_name)
for index in filename_list.index:
    # 读入csv文件    
    file_name = os.path.join(data_folder, filename_list['文件名称'][index])
    table_name = filename_list['file_name'][index]    
    print('--  处理第 %s 张表：%s'%(index +1, table_name))
    data = pd.read_csv(file_name,nrows =5) 
    
    field = [x + ' string' for x in data.columns.tolist()]
    
    # 在hive上建立标准表 
    cursor.execute('drop table if exists %s;' %table_name)     
    sql_code  =  "create external table if not exists {0}{1}".\
            format(table_name,tuple(field)).replace("'","") \
            + '\n' + "ROW FORMAT DELIMITED FIELDS TERMINATED BY ','" \
            + '\n' + "LOCATION '/tmp/jxg_data/{0}'".format(table_name)    
    print(sql_code)
    try :
        cursor.execute(sql_code)
    except Exception as e:
        print(e)
        print(table_name)
        
    file.write("hdfs dfs -put -f '/mnt/disk2/jxg_data/{1}.csv' '/tmp/jxg_data/{1}'".\
               format(database_name,table_name) + "\n")    

file.close()        