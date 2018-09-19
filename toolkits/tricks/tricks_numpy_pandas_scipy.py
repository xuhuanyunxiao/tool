# -*- coding: utf-8 -*-

#%% -----------------     pandas  ----------------------
import pandas as pd

names = locals()

pd.set_option('display.max_colwidth',1000) # 显示列数
pd.set_option('precision', 3) # 设置精度
pd.set_option('display.float_format', lambda x:'%.3f' %x) # 不采用科学计数法显示

import warnings  #  -----------------
warnings.filterwarnings('ignore') # 为了整洁，去除弹出的warnings

# 分割DataFrame中的某列数据  -----------------
users_data = pd.DataFrame((str(x).split('::') for x in pd.DataFrame(users).iloc[:,0]),
                          columns = 'UserID::Gender::Age::Occupation::Zip-code'.split('::'))

stat = pd.pivot_table(students_list,index=["性别","民族","党派"],columns=["省份"],
                      values=["计数"],aggfunc=np.sum,
                      fill_value=0,margins=True)

province = place[place['symbol'].str.contains('0000')]
province.columns = ['province_symbol','province_name']

# 以下相似  -----------------
province['for_coun'] = province['province_symbol'].apply(lambda x:x[0:2])
combined_data['city_class'] = combined_data['城市级别'].apply(decide_class1) # decide_class1 自建函数
cleaned_data['年份1'] = [decide_value(value) for value in cleaned_data[['体检年','年份']].values] # decide_value 自建函数

place_matrix = pd.merge(place_matrix,district,left_on = 'for_dist', right_on = 'for_coun')

place_matrix['county_name'][place_matrix['county_name'] =='城区'] = \
place_matrix['district_name'][place_matrix['county_name'] =='城区'] + '_' + \
place_matrix['county_name'][place_matrix['county_name'] =='城区'] 

useful_data['学段'] = useful_data['年级'].map({1:'小学低年级', 
                   2:'小学低年级',3:'小学中年级',4:'小学中年级', 5:'小学高年级',
                   6:'小学高年级',7:'初中',8:'初中',9:'初中', 10:'高中', 11:'高中', 12:'高中'})

clearn_data = clearn_data[clearn_data['年级'].isin(ex_list)]

# 多列运算
kfold_result['R_W'] = kfold_result.apply(lambda x: 'Right' if x['label'] == x['predict_label'] else 'Wrong', axis = 1)

# 转换数据  -----------------
ages_data = grade_data[[True if (age[g-1] <= int(item) & int(item) <= age[g-1+4] ) else False 
                   for item in grade_data['年龄']]]
stability_samples = stability_samples[(stability_samples['年份'] != 2010)  | (stability_samples['年级'] != 11)]
circ_cor['publishtime'] = circ_cor['publishtime'].apply(lambda x: x.strftime("%Y-%m-%d %H-%M-%S"))


# 用元组数据做index  -----------------
tuples = useful_data.columns.tolist()
tupless = [i for i in tuples if (i[1] == value_name) |(i[0] =='年级')|(i[0] =='年龄')|(i[0] =='学段')]
useful_data = useful_data.reindex(columns=pd.MultiIndex.from_tuples(tupless))

# 插入列
kfold_result.insert(0, '备注', '') # 第0列，列名，该列的值

# 将某列设为index
address_matrix = pd.DataFrame(address_matrix, columns = ['index','城市级别','城市名']).drop_duplicates(subset=['index']).set_index('index')

# 准确内存大小  -----------------
company_regis_capital.info(memory_usage = 'deep') 
table_data_commom['exist_days'].value_counts(dropna = False)

# 读取数据、保存数据  -----------------
# 分块读取
reader = pd.read_table('tmp.sv', sep='|', chunksize=4)
for chunk in reader: print(chunk)
# 迭代读取
chunks = pd.read_csv('train.csv',iterator = True)
chunk = chunks.get_chunk(5)

with pd.ExcelWriter(fea_filename) as writer:
    single_fea_desc.to_excel(writer,'各个特征')
    writer.save()
 

# json
df = pd.DataFrame([['a', 'b'], ['c', 'd']], 
    index=['row 1', 'row 2'],
    columns=['col 1', 'col 2'])
df.to_json(orient='records')
# [{"col 1":"a","col 2":"b"},{"col 1":"c","col 2":"d"}]
df.to_json(orient='split')
df.to_json(orient='index')
# {"row 1":{"col 1":"a","col 2":"b"},"row 2":{"col 1":"c","col 2":"d"}}
df.to_json(orient='columns')
# {"col 1":{"row 1":"a","row 2":"c"},"col 2":{"row 1":"b","row 2":"d"}}
df.to_json(orient='values')
df.to_json(orient='table')

# dict
df.to_dict('records')
# [{'col1': 1.0, 'col2': 0.5}, {'col1': 2.0, 'col2': 0.75}]
# dict to DataFarme
pd.DataFrame.from_dict(circ_stat[0], orient='index' ) 

# 随机取样
DataFrame.sample(n=None, frac=None, replace=False, 
    weights=None, random_state=None, axis=None)


#%% -----------------     numpy  ----------------------
import numpy as np



#%% -----------------     scipy  ----------------------










