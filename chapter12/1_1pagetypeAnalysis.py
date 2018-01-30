
# coding: utf-8

# In[1]:


### 第一部分 ###：数据探索分析——网页类型分析

import pandas as pd
from sqlalchemy import create_engine

# 先自定义函数将表格写入数据库里，以备操作过程中有些数据要写入数据库
def savetosql(DF,tablename):
    import pandas as pd
    from sqlalchemy import create_engine
    yconnect = create_engine('mysql+mysqldb://root:@127.0.0.1:3306/jing?charset=utf8')  
    pd.io.sql.to_sql(DF,tablename, yconnect, schema='jing', if_exists='append')  


# In[2]:

# python 访问数据库
engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/jing?charset=utf8')
sql = pd.read_sql('all_gzdata', engine, chunksize = 10000)
# '''
# 由于本人电脑用的主机Host名称为：127.0.0.1，端口3306，使用的数据库名称为test,字符集为utf8，用户名为root,密码为空,所以配置如上所示
# 用create_engine建立连接，连接地址的意思依次为“数据库格式（mysql）+程序名（pymysql）+账号密码@地址端口/数据库名（test）”，最后指定编码为utf8；
# all_gzdata是表名，engine是连接数据的引擎，chunksize指定每次读取1万条记录。这时候sql是一个容器，未真正读取数据。

# '''
# realIP`, `realAreacode`, `userAgent`, `userOS`, 
# `userID`, `clientID`, `timestamp`, `timestamp_format`,
# `pagePath`, `ymd`, `fullURL`, `fullURLId`, `hostname`, 
# `pageTitle`, `pageTitleCategoryId`, `pageTitleCategoryName`,
# `pageTitleKw`, `fullReferrer`, `fullReferrerURL`, `organicKeyword`, `source`

#-----* 1 *----- 统计各个网页类型所占的比例

counts1 = [ i['fullURLId'].value_counts() for i in sql] #逐块统计
counts1


# In[3]:

counts1 = pd.concat(counts1).groupby(level=0).sum() #合并统计结果，把相同的统计项合并（即按index分组并求和）
counts1


# In[4]:

counts1 = counts1.reset_index() #重新设置index，将原来的index作为counts的一列。
counts1


# In[5]:

counts1.columns = ['index', 'num'] #重新设置列名，主要是第二列，默认为0
counts1['type'] = counts1['index'].str.extract('(\d{3})') #提取前三个数字作为类别id（！！！）
counts1


# In[6]:

counts1_ = counts1[['type', 'num']].groupby('type').sum() #按类别合并
counts1_.sort_values(by='num', ascending=False,inplace=True) #降序排列
counts1_['percentage'] = (counts1_['num']/counts1_['num'].sum())*100

#保存的表名命名格式为“1_1_k此表功能名称”，此表表示生成的第1张表格，功能为type_counts：计算各个大类占的比例
counts1_.to_excel('1_1_1type_counts.xlsx') 
counts1_


# In[7]:

# 每个大类别下面小类别占比
a = counts1.set_index(['type'])
b = counts1.groupby('type').sum()
c = pd.merge(a,b,left_index=True,right_index=True)
c


# In[8]:

c['persentage'] = (c['num_x']/c['num_y'])*100
del c['num_y']
c.rename(columns={'num_x':'num'},inplace=True)
c


# In[9]:

c.reset_index(inplace = True)
d = c.sort_values(by=['type','persentage'],ascending=[True,False]).reset_index()
d


# In[10]:


del d['level_0']
per_counts= d.set_index(['type','index'])
#保存的表名命名格式为“1_1_k+此表功能名称”，此表表示生成的第2张表格，功能为type_counts_per，计算每个大类下各个小分支所占比例
per_counts.to_excel('1_1_2type_counts_per.xlsx')
per_counts


# In[11]:

#-----* 2 *----- 统计知识类型（107类别）内部的点击情况

# 因为只有107001一类，但是可以继续细分成三类：知识内容页、知识列表页、知识首页
def count107(i): #自定义统计函数
    j = i[['fullURL']][i['fullURLId'].str.contains('107')].copy() #找出类别包含107的网址
    j['type'] = None # 添加空列
    j['type'][j['fullURL'].str.contains('info/.+?/')]= u'知识首页'
    j['type'][j['fullURL'].str.contains('info/.+?/.+?')]= u'知识列表页'
    j['type'][j['fullURL'].str.contains('/\d+?_*\d+?\.html')]= u'知识内容页'
    return j['type'].value_counts()
# 注意：获取一次sql对象就需要重新访问一下数据库(!!!)
engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/jing?charset=utf8')
sql = pd.read_sql('all_gzdata', engine, chunksize = 10000)

counts2 = [count107(i) for i in sql] # 逐块统计
counts2 = pd.concat(counts2).groupby(level=0).sum() # 合并统计结果
counts2


# In[12]:

#计算各个部分的占比
res107 = pd.DataFrame(counts2)
# res107.reset_index(inplace=True)
res107.index.name= u'107类型'
res107.rename(columns={'type':'num'},inplace=True)
res107[u'百分比'] = (res107['num']/res107['num'].sum())*100
res107.reset_index(inplace = True)
#保存的表名命名格式为“1_1_k+此表功能名称”，此表表示生成的第3张表格，功能为type107，计算知识类型各个小类型所占比例
res107.to_excel('1_1_3type107.xlsx')
res107


# In[13]:

#-----* 3 *----- 统计带"?"问号网址类型统计

# 注意获取一次sql对象就需要重新访问一下数据库

def countquestion(i): #自定义统计函数
    j = i[['fullURLId']][i['fullURL'].str.contains('\?')].copy() #找出类别包含107的网址
    return j

engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/jing?charset=utf8')
sql = pd.read_sql('all_gzdata', engine, chunksize = 10000)

counts3 = [countquestion(i)['fullURLId'].value_counts() for i in sql]
counts3 = pd.concat(counts3).groupby(level=0).sum()
counts3


# In[14]:

# 求各个类型的占比并保存数据
df1 =  pd.DataFrame(counts3)
df1['perc'] = df1['fullURLId']/df1['fullURLId'].sum()*100
df1.sort_values(by='fullURLId',ascending=False,inplace=True)
#保存的表名命名格式为“1_1_k+此表功能名称”，此表表示生成的第4张表格，功能为questiontype，计算所有带问号页面各个类型的占比
df1.round(4).to_excel('1_1_4questiontype.xlsx')
df1.round(4)


# In[15]:

# 求带问号的结果占所有数据的比例
from __future__ import division
allcount = counts1['num'].sum()#所有记录总数
df1['fullURLId'].sum()/allcount*100 #7.820407188488865


# In[16]:

#-----* 4 *----- 统计199类型中的具体类型占比

def page199(i): #自定义统计函数
    j = i[['fullURL','pageTitle']][(i['fullURLId'].str.contains('199')) & (i['fullURL'].str.contains('\?'))]
    j['pageTitle'].fillna(u'空',inplace=True)
    j['type'] = u'其他' # 添加空列
    j['type'][j['pageTitle'].str.contains(u'法律快车-律师助手')]= u'法律快车-律师助手'
    j['type'][j['pageTitle'].str.contains(u'咨询发布成功')]= u'咨询发布成功'
    j['type'][j['pageTitle'].str.contains(u'免费发布法律咨询' )] = u'免费发布法律咨询'
    j['type'][j['pageTitle'].str.contains(u'法律快搜')] = u'快搜'
    j['type'][j['pageTitle'].str.contains(u'法律快车法律经验')] = u'法律快车法律经验'
    j['type'][j['pageTitle'].str.contains(u'法律快车法律咨询')] = u'法律快车法律咨询'
    j['type'][(j['pageTitle'].str.contains(u'_法律快车')) | (j['pageTitle'].str.contains(u'-法律快车'))] = u'法律快车'
    j['type'][j['pageTitle'].str.contains(u'空')] = u'空'
    
    return j
# 注意：获取一次sql对象就需要重新访问一下数据库
engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/jing?charset=utf8')
sql = pd.read_sql('all_gzdata', engine, chunksize = 10000)# 分块读取数据库信息

counts4 = [page199(i) for i in sql] # 逐块统计
counts4 = pd.concat(counts4)
d1 = counts4['type'].value_counts()
print d1
d2 = counts4[counts4['type']==u'其他']
savetosql(d2,'199elsePercentage')# 将199的网页中的“其他”类型的数据存到数据库中


# In[17]:

# 求各个部分的占比并保存数据
df1_ =  pd.DataFrame(d1)
df1_['perc'] = df1_['type']/df1_['type'].sum()*100
df1_.sort_values(by='type',ascending=False,inplace=True)
#保存的表名命名格式为“1_1_k+此表功能名称”，此表表示生成的第5张表格，功能为page199，计算199类型中的具体类型占比
df1_.to_excel('1_1_5page199.xlsx')
df1_


# In[18]:

#-----* 5 *----- 统计瞎逛用户中各个类型占比（没有具体的网页以.html后缀结尾）

def xiaguang(i): #自定义统计函数
    j = i[['fullURL','fullURLId','pageTitle']][(i['fullURL'].str.contains('\.html'))==False]
    return j

# 注意获取一次sql对象就需要重新访问一下数据库
engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/jing?charset=utf8')
sql = pd.read_sql('all_gzdata', engine, chunksize = 10000)# 分块读取数据库信息

counts5 = [xiaguang(i) for i in sql]
counts5 = pd.concat(counts5)

# 将瞎逛的值保存到数据库表中
savetosql(counts5,'xiaguang')# 将199的网页中的“其他”类型的数据存到数据库中

xg1 = counts5['fullURLId'].value_counts()
xg1


# In[19]:

# 求各个部分的占比并保存数据
xg_ =  pd.DataFrame(xg1)
xg_.reset_index(inplace=True)
xg_.columns= ['index', 'num']
xg_['perc'] = xg_['num']/xg_['num'].sum()*100
xg_.sort_values(by='num',ascending=False,inplace=True)

xg_['type'] = xg_['index'].str.extract('(\d{3})') #提取前三个数字作为类别id    

xgs_ = xg_[['type', 'num']].groupby('type').sum() #按类别合并
xgs_.sort_values(by='num', ascending=False,inplace=True) #降序排列
xgs_['percentage'] = xgs_['num']/xgs_['num'].sum()*100

#保存的表名命名格式为“1_1_k+此表功能名称”，此表表示生成的第6张表格，功能为xiaguang，计算瞎逛用户中各个类型占比
xgs_.round(4).to_excel('1_1_6xiaguang.xlsx')
xgs_.round(4)


# In[ ]:




# In[ ]:




# In[ ]:



