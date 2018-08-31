#!/usr/bin/env python
# -*- coding: utf-8 -*-

#%%
'''
命名规则：
1 变量：普通 this_is_a_var、全局 GLOBAL_VAR_NAME
2 包名 & 模块名：package_name、module_name.py
3 函数 & 方法：function_name()、method_name()
4 类名 & 异常：ClassName、ExceptonName
5 常量：MAX_OVERFLOW

模块内容的顺序：
    模块说明和docstring — import — globals&constants — 其他定义;
其中import部分:
    又按标准、三方和自己编写顺序依次排放，之间空一行。
    
使用：
    import toolkits  # toolkits.specific_func.contain_ch('salskdj中文')
    from toolkits.specific_func import set_ch_pd
    
文档测试：
def multiply(a, b):
    """
    >>> multiply(4, 3)
    12
    >>> multiply('a', 3)
    'aaa'
    """
    return a * b

import doctest
doctest.testmod(verbose=True)
'''

num=['零','一','二','三','四','五','六','七','八','九']  
kin=['十','百','千','万','零']  
#import time  
  
def sadd(x):  
    x.reverse()  
    if len(x) >= 2:  
        x.insert(1,kin[0])  
        if len(x) >= 4:  
            x.insert(3,kin[1])  
            if len(x) >= 6:  
                x.insert(5,kin[2])  
                if len(x) >= 8:  
                    x.insert(7,kin[3])  
                    if len(x) >= 10:  
                        x.insert(9,kin[0])  
                        if len(x) >= 12:  
                            x.insert(11,kin[1])  
  
    x=fw(x)  
    x=d1(x)  
    x=d2(x)  
    x=dl(x)  
    return x  
      
def d1(x):  
    if '零' in x:  
        a=x.index('零')  
        if a==0:  
            del x[0]  
            d1(x)  
        else:  
            if x[a+2] in ['十','百','千','万','零']:  
                if x[a+1] != '万':  
                    del x[a+1]  
                    d1(x)       
    return x  
def d2(x):  
    try:  
        a=x.index('零')  
        if x[a-1] in ['十','百','千','零']:  
            del x[a-1]  
            d2(x[a+1])  
    except:pass  
    return x  
  
def fw(x):  
    if len(x) >= 9:  
        if x[8] == '零':  
            del x[8]  
    return x  
def dl(x):  
    try:  
        if x[0]=='零':  
            del x[0]  
            d1(x)  
    except:pass  
    x.reverse()  
    x=''.join(x)  
    return x  

#%% 测试将0至9999999全部转换成汉子的时间，80s左右
#def rankis():  
#    rank=[]  
#    for i in range(9999999):  
#        i=list(str(i))  
#        for j in i:  
#            i[(i.index(j))]=num[int(j)]  
#        i=sadd(i)  
#        rank.append(i)  
#    return rank 

#%%  转换某一个数字成汉字
def num_to_chinese(number):  
    i = number
    i=list(str(i))  
    for j in i:  
        i[(i.index(j))]=num[int(j)]  
    i=sadd(i)   
    return i 
#%%
#start=time.time()  
#rank=rankis(123)  
#end=time.time()-start  
#print('程序共用时：%0.2f'%end)  



def transform_alabo2_roman_num(one_num):  
    ''''' 
    将阿拉伯数字转化为罗马数字 
    '''  
    num_list=[1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]  
    str_list=["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]  
    res=''  
    for i in range(len(num_list)):  
        while one_num>=num_list[i]:  
            one_num-=num_list[i]  
            res+=str_list[i]  
    return res  
  
  
def transform_roman_num2_alabo(one_str):  
    ''''' 
    将罗马数字转化为阿拉伯数字 
    '''  
    define_dict={'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}  
    if one_str=='0':  
        return 0  
    else:  
        res=0  
        for i in range(0,len(one_str)):  
            if i==0 or define_dict[one_str[i]]<=define_dict[one_str[i-1]]:  
                res+=define_dict[one_str[i]]  
            else:  
                res+=define_dict[one_str[i]]-2*define_dict[one_str[i-1]]  
        return res  
        # #下面这种写法也可以  
        # for i in range(len(one_str)):  
        #     if i > 0 and define_dict[one_str[i]] > define_dict[one_str[i - 1]]:  
        #         res -= define_dict[one_str[i - 1]]  
        #         res += define_dict[one_str[i]] - define_dict[one_str[i - 1]]  
        #     else:  
        #         res += define_dict[one_str[i]]  
        # return res  
  
  
if __name__ == '__main__':  
    print('**************将罗马数字转化为阿拉伯数字**************'  )
    one_str_list=['DII','XV','MDCLXVI','XII','VIII','XCIX','XII']  
    for one_str in one_str_list:  
        print(one_str,'----->',transform_roman_num2_alabo(one_str)  )
      
    print('**************将阿拉伯数字转化为罗马数字**************'  )
    one_num_list=[77,66,55,8,1200,34,65,3,21,99]  
    for one_num in one_num_list:  
        print(one_num,'----->',transform_alabo2_roman_num(one_num)  )