
# coding: utf-8

# In[1]:


### 第一部分 ###：数据探索分析——点击次数分析

# 目标：点击次数分析：统计分析原始数据用户浏览网页次数（以“真实IP”区分）的情况
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

# 读取数据库数据
engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/jing?charset=utf8')
sql = pd.read_sql('all_gzdata', engine, chunksize = 10000)


#-----* 1 *-----统计点击次数

counts1 = [i['realIP'].value_counts() for i in sql] # 分块统计各个IP的出现次数
counts1 = pd.concat(counts1).groupby(level=0).sum() # 合并统计结果，level=0表示按照index分组

counts1


# In[3]:

counts1_ = DataFrame(counts1)
counts1_[1]=1 # 添加1列全为1
a = counts1_.groupby('realIP').sum()#统计各个“不同点击次数”分别出现的次数# 也可以使用counts1_['realIP'].value_counts()功能
a.columns=[u'用户数']
a.index.name = u'点击次数'
a[u'用户百分比'] = a[u'用户数']/a[u'用户数'].sum()*100
a[u'记录百分比'] = a[u'用户数']*a.index/counts1_['realIP'].sum()*100
a.sort_index(inplace = True)
b = a.iloc[:7,:]
c = b.T
c


# In[4]:

#-----* 2 *-----统计1~7次数及7次以上的
c.insert(0,u'总计',[a[u'用户数'].sum(),100,100])
c[u'7次及以上'] = c.iloc[:,0]- c.iloc[:,1:].sum(1)
#保存的表名命名格式为“1_1_k此表功能名称”，此表表示生成的第1张表格，功能为clickTimes：统计网页点击情况
c.to_excel('1_2_1clickTimes.xlsx')
c


# In[5]:

# 转置表格，并将所有输出保留两位小数
d = c.T
format = lambda x: '%.2f' % x  # 也可以使用d.round(4)
d = d.applymap(format)
d


# In[20]:

# 分析浏览次数7次以上的数据
times = counts1_.index[7:]
bins = [7,100,1000,50000]
cats = pd.cut(times,bins,right=True,labels=['8~100','101~1000','1000以上'])
e = cats.value_counts()
e = DataFrame(e, columns =[u'用户数'])
e.index.name = u'点击次数'


# In[22]:

e[u'用户数'] = np.nan
e.ix[u'8~100',u'用户数'] = a.loc[8:100,:][u'用户数'].sum()
e.ix['101~1000',u'用户数'] = a.loc[101:1000,:][u'用户数'].sum()
e.ix['1000以上',u'用户数'] = a.loc[1001:,:][u'用户数'].sum()
e.sort_values(by=u'用户数',ascending=False,inplace = True)
e.reset_index(inplace=True)

e


# In[23]:

#-----* 3 *-----对浏览一次的用户行为进行分析

# 读取数据库数据
engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/jing?charset=utf8')
sql = pd.read_sql('all_gzdata', engine, chunksize = 10000)


# In[24]:

# 获取浏览一次的所有数据
f = counts1_[counts1_['realIP']==1]
del f[1]
f.columns = [u'点击次数']
f.index.name = 'realIP'
# g = [pd.merge(f,i[['fullURLId','fullURL','realIP']],right_on = 'realIP',left_index=True,how ='left') for i in sql]
g = [i[['fullURLId','fullURL','realIP']] for i in sql]
g = pd.concat(g)
h = pd.merge(f,g,right_on = 'realIP',left_index=True,how ='left')
h


# In[28]:

# 浏览一次的用户的网页类型ID分析
i = h['fullURLId'].value_counts()
i = DataFrame(i)
i.rename(columns={'fullURLId':u'个数'},inplace=True)
i.index.name = u'网页类型ID'
i[u'百分比'] = i[u'个数']/i[u'个数'].sum()*100

#保存的表名命名格式为“1_2_k此表功能名称”，此表表示生成的第2张表格，功能为typeID：浏览一次的用户的网页类型ID分析
i.to_excel('1_2_2typeID.xlsx')
i


# In[29]:

j = i[i[u'个数']>100]
j


# In[27]:

j.loc[u'其他',u'个数'] = i[i[u'个数']<=100][u'个数'].sum()
j.loc[u'其他',u'百分比'] = 100-i[i[u'个数']>100][u'百分比'].sum()
j# 浏览一次的用户中浏览的网页类型ID


# In[30]:

#　点击1次用户浏览网页统计(点击数大于100次的)
k = DataFrame(h['fullURL'].value_counts())
k.index.name = u'网址'
k.columns = [u'点击数']
m = k[k[u'点击数'] > 100]
m.loc[u'其他',u'点击数'] = k[k[u'点击数']<=100][u'点击数'].sum()
m[u'百分比'] = m[u'点击数']/k[u'点击数'].sum()
#保存的表名命名格式为“1_2_k此表功能名称”，此表表示生成的第3张表格，功能为lookMorethan100：点击1次用户浏览网页统计(点击数大于100次的)
m.to_excel('1_2_3lookMorethan100.xlsx')
m


# In[ ]:




# In[ ]:



