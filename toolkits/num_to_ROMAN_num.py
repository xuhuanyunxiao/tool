# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 11:08:16 2018

@author: Administrator
"""

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