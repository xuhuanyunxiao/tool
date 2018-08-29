# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 10:49:30 2017

@author: xh
"""

#%% -----------------     BeautifulSoup、urllib  ----------------------
# 网络：获取六级城市群名称
from bs4 import BeautifulSoup
import urllib

from Tookits.specific_func import find_punctuation

url = 'https://baike.baidu.com/item/%E4%B8%AD%E5%9B%BD%E5%9F%8E%E5%B8%82%E6%96%B0%E5%88%86%E7%BA%A7%E5%90%8D%E5%8D%95/12702007?fr=aladdin#2_6'
response = urllib.request.urlopen(url)
soup = BeautifulSoup(response, 'html.parser', from_encoding='utf-8')

city_name = soup.find_all('div',attrs={'class':'para','label-module':"para"})
city_na = [c.get_text() for c in city_name]
c_names = [city_na[10],city_na[12],city_na[14],city_na[16],city_na[18],city_na[20]]
city = []
for c in c_names:
    punctuation = find_punctuation(pd.Series(c), pattern = u'[\u4e00-\u9fa5]*', del_punc = r'[、]*') # 去除汉字
    if punctuation:
        for p in list(punctuation):c = c.replace(p,'')
    city.append(c.split('、'))

# 本地：获取中国行政区所有省、地区、县的名称
local_url = data_folder + '\\最新县及县以上行政区划代码（截止2016年7月31日）.html'

html = open(local_url, encoding='utf-8')
html_content = html.read()

soup = BeautifulSoup(html_content, 'html.parser', from_encoding='utf-8')

place_name = soup.find_all('p',attrs={'class':'MsoNormal'})
place_n = [p.get_text().split(' ') for p in place_name]
place = pd.DataFrame(place_n, columns = ['symbol','name']).applymap(lambda x: str(x).strip())



