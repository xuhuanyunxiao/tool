


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
print(test_set.shape)
print(test_set.head())
import json
sample_num = 1000
with open("data/20180718_test_set(%s).json"%sample_num,'w',encoding='utf-8') as json_file:
    json.dump({"record":test_set.iloc[600:1000,:4].to_dict(orient='records')} ,json_file,ensure_ascii=False)