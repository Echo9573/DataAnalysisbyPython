
# coding: utf-8

# In[1]:


### 第二部分 ###：数据预处理

#　数据清洗
import pandas as pd
import numpy as np
from pandas import Series,DataFrame
from sqlalchemy import create_engine
import MySQLdb as msd
# 先自定义函数将表格写入数据库里，以备操作过程中有些数据要写入数据库
def savetosql(DF,tablename):
    import pandas as pd
    from sqlalchemy import create_engine
    yconnect = create_engine('mysql+mysqldb://root:@127.0.0.1:3306/jing?charset=utf8')  
    pd.io.sql.to_sql(DF,tablename, yconnect, schema='jing', if_exists='append')  


# In[2]:

#-----* 1 *-----查看各个需要删除的规则包含的信息

# 删除规则1：统计中间类型网页（带midques_关键字）
# 读取数据库数据
engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/jing?charset=utf8')
sql = pd.read_sql('all_gzdata', engine, chunksize = 10000)

def countmidques(i): 
    j = i[['fullURL','fullURLId','realIP']].copy()
    j['type'] = u'非中间类型网页'
    j['type'][j['fullURL'].str.contains('midques_')]= u'中间类型网页'
    return j['type'].value_counts()
counts1 = [countmidques(i) for i in sql]
counts1 = pd.concat(counts1).groupby(level=0).sum()
counts1


# In[3]:

# 删除规则2：主网址去掉无.html点击行为的用户记录
# 读取数据库数据
engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/jing?charset=utf8')
sql = pd.read_sql('all_gzdata', engine, chunksize = 10000)

def countnohtml(i):
    j = i[['fullURL','pageTitle','fullURLId']].copy()
    j['type'] = u'有html页面'
    j['type'][j['fullURL'].str.contains('\.html')==False] = u'无.html点击行为的用户记录'
    
    return j['type'].value_counts()
counts2 = [countnohtml(i) for i in sql]
counts2 = pd.concat(counts2).groupby(level=0).sum()
counts2


# In[4]:

# 删除规则3：主网址是律师的浏览信息网页（快车-律师助手）、咨询发布成功、快搜免费发布法律
# 读取数据库数据
# *备注：此规则中要删除的记录的网址均不含有.html，所以，规则三需要过滤的信息包含了规则2中需要过滤的
engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/jing?charset=utf8')
sql = pd.read_sql('all_gzdata', engine, chunksize = 10000)

def countothers(i): 
    j = i[['fullURL','pageTitle','fullURLId']].copy()
    j['type'] = u'其他'   
    j['pageTitle'].fillna(u'空',inplace=True)
    j['type'][j['pageTitle'].str.contains(u'快车-律师助手')]= u'快车-律师助手'
    j['type'][j['pageTitle'].str.contains(u'咨询发布成功')]= u'咨询发布成功'
    j['type'][(j['pageTitle'].str.contains(u'免费发布法律咨询')) | (j['pageTitle'].str.contains(u'法律快搜'))] = u'快搜免费发布法律咨询'
    
    return j['type'].value_counts()
counts3 = [countothers(i) for i in sql]
counts3 = pd.concat(counts3).groupby(level=0).sum()
counts3


# In[5]:

# 删除规则4: 去掉网址中问号后面的部分，截取问号前面的部分;去掉主网址不包含关键字
engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/jing?charset=utf8')
sql = pd.read_sql('all_gzdata', engine, chunksize = 10000)

def deletquesafter(i):
    j = i[['fullURL']].copy()
    j['fullURL'] = j['fullURL'].str.replace('\?.*','')
    j['type'] = u'主网址不包含关键字'
    j['type'][j['fullURL'].str.contains('lawtime')] = u'主网址包含关键字'
    return j

counts4 = [deletquesafter(i) for i in sql]
counts4 = pd.concat(counts4)
print len(counts4)
counts4['type'].value_counts()


# In[6]:

# 删除规则5: 重复数据去除
# 读取数据库数据
engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/jing?charset=utf8')
sql = pd.read_sql('all_gzdata', engine, chunksize = 10000)

def countduplicate(i): 
    j = i[['fullURL','timestamp_format','realIP']].copy()
    return j

counts5 = [countduplicate(i) for i in sql]
counts5 = pd.concat(counts5)

print len(counts5[counts5.duplicated()==True])
print len(counts5.drop_duplicates())
a = counts5.drop_duplicates()


# In[7]:

#-----* 2 *-----Python访问数据库进行清洗操作
# 第一步，完成删除规则1，2，4

# 对网址的操作 （只要.html结尾的 & 截取问号左边的值 & 只要包含主网址（lawtime)的&网址中间没有midques_的
# 读取数据库数据
engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/jing?charset=utf8')
sql = pd.read_sql('all_gzdata', engine, chunksize = 10000)

for i in sql:
    d = i[['realIP', 'fullURL','pageTitle','userID','timestamp_format']].copy() # 只要网址列
    d['fullURL'] = d['fullURL'].str.replace('\?.*','') # 网址中问号后面的部分
    d = d[(d['fullURL'].str.contains('\.html')) & (d['fullURL'].str.contains('lawtime')) & (d['fullURL'].str.contains('midques_') == False)] # 只要含有.html的网址
    # 保存到数据库中
    d.to_sql('cleaned_one', engine, index = False, if_exists = 'append')


# In[8]:

# 第二步，完成删除规则3

# 对网页标题的操作 （删除 快车-律师助手 & 免费发布法律咨询 & 咨询发布成功 & 法律快搜）
# 读取数据库数据（基于操作1之后）
engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/jing?charset=utf8')
sql = pd.read_sql('cleaned_one', engine, chunksize = 10000)

# 对网址的操作 （只要.html结尾的&只要包含主网址（lawtime)的&网址中间没有midques_的
for i in sql:
    d = i[['realIP','fullURL','pageTitle','userID','timestamp_format']]# 只要网址列
    d['pageTitle'].fillna(u'空',inplace=True)
    d = d[(d['pageTitle'].str.contains(u'快车-律师助手') == False) & (d['pageTitle'].str.contains(u'咨询发布成功') == False) &           (d['pageTitle'].str.contains(u'免费发布法律咨询') == False) & (d['pageTitle'].str.contains(u'法律快搜') == False)         ].copy()
    # 保存到数据库中
    d.to_sql('cleaned_two', engine, index = False, if_exists = 'append')
    
##### 注意：最后发现，对于网页标题需要进行的删除的记录的网址中，均没有.html，因此，操作2可以不必做，操作1已完成工作


# In[9]:

# 第三步，完成删除规则5

# 删除重复记录
# 读取数据库数据（基于第二步之后）
engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/jing?charset=utf8')
sql = pd.read_sql('cleaned_two', engine, chunksize = 10000)

def dropduplicate(i): 
    j = i[['realIP','fullURL','pageTitle','userID','timestamp_format']].copy()
    return j

count6 = [dropduplicate(i) for i in sql]
count6 = pd.concat(count6)
print len(count6)
count7 = count6.drop_duplicates(['fullURL','userID','timestamp_format'])
print len(count7)
savetosql(count7, 'cleaned_three')


# In[10]:

#-----* 3 *----- 查看进行删除操作后的表中的总记录数
# 查看all_gzdata表中的记录数
engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/jing?charset=utf8')
sql = pd.read_sql('all_gzdata', engine, chunksize = 10000)
lens = 0
for i in sql:
    temp = len(i)
    lens = temp + lens
print lens # 837450

# 查看cleaned_one表中的记录数
engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/jing?charset=utf8')
sql1 = pd.read_sql('cleaned_one', engine, chunksize = 10000)
lens1 = 0
for i in sql1:
    temp = len(i)
    lens1 = temp + lens1
print lens1 # 670965

# 查看cleaned_two表中的记录数
engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/jing?charset=utf8')
sql2 = pd.read_sql('cleaned_two', engine, chunksize = 10000)
lens2 = 0
for i in sql2:
    temp = len(i)
    lens2 = temp + lens2
print lens2 # 670965

# 查看cleaned_three表中的记录数
engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/jing?charset=utf8')
sql3 = pd.read_sql('cleaned_three', engine, chunksize = 10000)
lens3 = 0
for i in sql3:
    temp = len(i)
    lens3 = temp + lens3
print lens3 # 647300


# In[ ]:



