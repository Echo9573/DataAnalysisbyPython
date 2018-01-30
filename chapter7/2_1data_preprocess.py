
# coding: utf-8


#  数据预处理

from __future__ import division
from pandas import DataFrame,Series
import pandas as pd

datafile = 'air_data.csv'#航空公司原始数据，第一行是属性名
data = pd.read_csv(datafile, encoding='utf-8')

# 1> 数据清洗 
# 丢弃掉票价为0的记录；丢弃票价为0、平均折扣不为零、总飞行公里大于0的记录

cleanedfile = 'cleaned.xlsx'

data1 = data[data['SUM_YR_1'].notnull()*data['SUM_YR_2'].notnull()] #票价非空值才保留,去掉空值

#只保留票价非零的，或者平均折扣率与总飞行公里数同时为零的记录
index1 = data1['SUM_YR_1'] != 0
index2 = data1['SUM_YR_2'] != 0
index3 = (data1['SEG_KM_SUM'] == 0) & (data1['avg_discount'] == 0)
data1 = data1[index1 | index2 | index3] #或关系

data1.to_excel(cleanedfile)
data2 = data1[['LOAD_TIME','FFP_DATE','LAST_TO_END','FLIGHT_COUNT','SEG_KM_SUM','avg_discount']]
data2.to_excel('datadecrese.xlsx')


# 2> 数据规约 
import numpy as np
data = pd.read_excel('datadecrese.xlsx')

data['L1'] = pd.to_datetime(data['LOAD_TIME']) - pd.to_datetime(data['FFP_DATE'])# 以纳秒为单位
# data['L3'] = data['L1'].astype('int64')/10**10/8640/30 # 此方法假定每个月是30天，这方法不准确
data['L3'] = data['L1']/np.timedelta64(1, 'M') # 将间隔时间转成月份为单位，注意，此处必须加一个中间变量 （****）

# 将表中的浮点类型保留至小数点后四为
# f = lambda x:'%.2f' % x
# data[['L3']]  = data[['L3']].applymap(f) # or data['L3'] = data['L3'].apply(f)
# data[['L3']]  = data[['L3']].astype('float64')# 注意:使用apply或applymap后，数据类型变成Object,若后续有需要需要在此进行类型转换

data["L3"] = data["L3"].round(2) # 等价于上面三句话，数据类型不变
data['LAST_TO_END'] = (data['LAST_TO_END']/30).round(2)
data['avg_discount'] = data['avg_discount'].round(2)

data.drop('L1', axis=1, inplace =True) # 删除中间变量
data.drop(data.columns[:2], axis=1, inplace =True) # 去掉不需要的u'LOAD_TIME', u'FFP_DATE'
data.rename(columns={'LAST_TO_END':'R','FLIGHT_COUNT':'F','SEG_KM_SUM':'M','avg_discount':'C','L3':'L'},inplace=True)
data.to_excel('sxgz.xlsx',index=False)

def f(x):
    return Series([x.min(),x.max()], index=['min','max'])
d = data.apply(f)
d.to_excel('summary_data.xlsx')

# 3> 数据标准化
#标准差标准化
d1 = pd.read_excel('sxgz.xlsx')
d2 = (d1-d1.mean())/d1.std()
d1 =d2.iloc[:,[4,0,1,2,3]]
d1.columns = ['Z'+i for i in d1.columns]#表头重命名
d1.to_excel('sjbzh.xlsx',index=False)

