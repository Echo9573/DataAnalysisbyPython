
# coding: utf-8


# 7.2 数据探索
#对数据进行基本的探索
#返回缺失值个数以及最大最小值
import pandas as pd

datafile = 'air_data.csv'#航空公司原始数据，第一行是属性名
result = 'explore.xlsx'

data = pd.read_csv(datafile, encoding='utf-8')
explore = data.describe( percentiles = [],include = 'all').T

explore['null'] = len(data)-explore['count']


explore1 = explore[['null','max','min']]
explore1.columns = [u'空值数',u'最大值',u'最小值']#重命名列名

explore1.to_excel(result)

