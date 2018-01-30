
# coding: utf-8

# In[1]:


# 属性规约：确定模型构建中需要的属性
import pandas as pd
import numpy as np
from pandas import Series,DataFrame
from sqlalchemy import create_engine
import MySQLdb as msd


# In[2]:

engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/jing?charset=utf8')
sql = pd.read_sql('changed_six', engine, chunksize = 10000)

for i in sql:
    j = i[['realIP','fullURL']].copy()
    j.to_sql('Allformodel_realIP', engine, index=False,if_exists = 'append')


# In[3]:

#  获取后续建模需要的数据  咨询（ask）和婚姻（hunyin）数据
# 读取数据库数据 
engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/jing?charset=utf8')
sql = pd.read_sql('changed_six', engine, chunksize = 10000)
l1 = 0
l2 = 0
for i in sql:
    zixun = i[['realIP','fullURL']][i['fullURL'].str.contains('(ask)|(askzt)')].copy()
#     l1 = len(zixun) + l1
    hunyin = i[['realIP','fullURL']][i['fullURL'].str.contains('hunyin')].copy()    
#     l2 = len(hunyin) + l2
    zixun.to_sql('zixunformodel', engine, index=False,if_exists = 'append')
    hunyin.to_sql('hunyinformodel', engine, index=False,if_exists = 'append')
# print l1,l2


# In[ ]:



