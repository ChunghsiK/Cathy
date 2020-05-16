#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd

#讀取全部相關檔案
df_a = pd.read_csv('a_lvr_land_a.csv')
df_b = pd.read_csv('b_lvr_land_a.csv')
df_e = pd.read_csv('e_lvr_land_a.csv')
df_f = pd.read_csv('f_lvr_land_a.csv')
df_h = pd.read_csv('h_lvr_land_a.csv')

#合併所有資料，並且重設index
df_all = pd.concat([df_a, df_b, df_e, df_f, df_h], ignore_index = True)


#去除第一列英文名稱
df_all = df_all.drop([0])


dic = {'一' : 1, '二' : 2, '三' : 3, '四' : 4, '五' : 5, '六' : 6, '七' : 7, '八' : 8, '九' : 9, '十': 10}

#新增欄位來記錄樓層數字
df_all['新']  = 0
df_all = df_all.fillna(value='Missing')


for index, row in df_all.iterrows():
    if len(row['總樓層數']) == 2:
        df_all.loc[index,'新'] = dic[row['總樓層數'][0]]
    elif len(row['總樓層數']) == 3:
        df_all.loc[index,'新'] = dic[row['總樓層數'][0]] + dic[row['總樓層數'][1]]
    elif len(row['總樓層數']) == 4:
        df_all.loc[index,'新'] = dic[row['總樓層數'][0]]*10 + dic[row['總樓層數'][2]]

#建立濾網過濾樓層數和用途
df_new = df_all[df_all['新'] >= 13]
f1 = df_new['主要用途'] == '住家用' 
df_new = df_new[f1]

#建立濾網過濾建物型態
df_new['f2'] = 0
for index, row in df_new.iterrows():
    if row['建物型態'][:4] == '住宅大樓':
        df_new.loc[index, 'f2'] = 1
df_new = df_new[df_new['f2'] == 1]

#刪除標記用欄位，並寫入filter_a
del df_new['新']
del df_new['f2']
df_new.to_csv(r'/Users/Hardy/Desktop/Programming/download/filter_a.csv', index = False, encoding='utf_8_sig')


df_fb = pd.read_csv('filter_a.csv')

#計算筆數和平均價位，寫入filter_b
index = df_fb.index
count = len(index)
cars = 0
total_price = 0
total_car_p = 0
for index, row in df_fb.iterrows():
    cars = cars + int(row['交易筆棟數'][-1])
    total_price = total_price + row['總價元']
    total_car_p = total_car_p + row['車位總價元']

df_output = pd.DataFrame({'總件數': [count], 
                          '總車位數': [cars], 
                          '平均總價元': [total_price/count], 
                          '平均車位總價元': [total_car_p/count]}) 

df_output.to_csv(r'/Users/Hardy/Desktop/Programming/download/filter_b.csv', index = False, encoding='utf_8_sig')