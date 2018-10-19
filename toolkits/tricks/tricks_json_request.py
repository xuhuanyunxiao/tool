


#%% -----------------     json  ----------------------
import json

# 一、将数据保存为.json文件
model={} #数据
with open("./hmm.json",'w',encoding='utf-8') as json_file:
        json.dump(model,json_file,ensure_ascii=False)  

# 二、读取.json文件
model={} #存放读取的数据
with open("./hmm.json",'r',encoding='utf-8') as json_file:
        model=json.load(json_file)

test_set['publishtime'] = test_set['publishtime'].apply(lambda x: x.strftime("%Y-%m-%d"))

sample_num = 1000
with open("data/20180718_test_set(%s).json"%sample_num,'w',encoding='utf-8') as json_file:
    json.dump({"record":test_set.iloc[600:1000,:4].to_dict(orient='records')} ,
    			json_file,ensure_ascii=False)



#%% -----------------     requests  ----------------------
import requests

def get_serve_data(day_list, sql_one_day, url, col_name):
    combined_data = pd.DataFrame()
    for day_select in day_list:
        print('-- day_select: ', day_select)
        mysql_data = pd.read_sql(eval(sql_one_day), engine)
        print('去空值前：', mysql_data.shape)
        mysql_data = mysql_data.drop_duplicates(subset = ['title', 'content'])
        print('去空值后：', mysql_data.shape)
        data = {"record":mysql_data.loc[:,['id', 'title' ,'content']].to_dict(orient = 'records')}
        
        parse_data, elapsed_time = get_server_res(data, url)
        print('elapsed_time: ', elapsed_time)
        
        parse_data.columns = ['id', 'predict_label']
        parse_data['predict_label'] = parse_data['predict_label'].apply(lambda x:class_name_dict[x])
        parse_data['label'] = ''
        combined_cor = pd.merge(parse_data, mysql_data, on = 'id', how = 'inner')
        combined_data = pd.concat([combined_data, combined_cor], axis = 0)

        print(combined_cor['predict_label'].value_counts())
    return combined_data

def get_server_res(data, url, col_name):
    '''
    服务器接口测试程序
    传入 dict, 传出 DataFrame
    '''
    # data = {'record':[{'id':0,'title':'ss','content':'zzz'},]}
    # data = {"record":marked_human_data.iloc[:5,:3].to_dict(orient = 'records')}
    # url "http://47.93.77.19:10000/correlation_negative"
    headers={'content-type':'application/json'}
    result = requests.post(url,
                      data = json.dumps(data),
                      headers=headers, allow_redirects=True)
    # print(result.text)
    json_data = json.loads(result.text)
    parse_data = []
    elapsed_time = json_data['elapsed_time']
    for i in range(len(json_data['docs'])):
        parse_data.append([json_data['docs'][i]['id'],
                          json_data['docs'][i][col_name]])
    parse_data = pd.DataFrame(parse_data, columns = ['id', col_name])    
    return parse_data, elapsed_time

combined_data['id'] = range(combined_data.shape[0])
combined_data['title'] = combined_data['title'].astype(str) 
combined_data['content'] = combined_data['content'].astype(str)
data = {"record":combined_data.loc[:,['id', 'title' ,'content']].to_dict(orient = 'records')}
url = "http://47.93.77.19:10000/judge_correlation_i"
col_name = 'cor'
parse_data, elapsed_time = get_server_res(data, url, col_name)
parse_data.columns = ['id', 'online_label']
parse_data.head()
