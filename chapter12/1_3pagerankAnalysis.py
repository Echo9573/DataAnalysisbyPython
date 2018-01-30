
# coding: utf-8

# In[1]:


# 目标：网页排名分析 获得各个网页点击率排名以及类型点击率排名：统计分析原始数据用户浏览网页次数（以“真实IP”区分）
# 第一部分：python 访问数据库
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

#-----* 1 *-----获取网页点击排名数

engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/jing?charset=utf8')
sql = pd.read_sql('all_gzdata', engine, chunksize = 10000)

def clickfreq(i): #自定义统计函数
    j = i[['fullURL','fullURLId','realIP']][i['fullURL'].str.contains('\.html')]
    return j

counts1 = [clickfreq(i) for i in sql] # 分块统计各个IP的出现次数
counts1 = pd.concat(counts1)

counts1_ = counts1['fullURL'].value_counts()
counts1_ = DataFrame(counts1_)


# In[3]:


counts1_.columns = [u'点击次数']
counts1_.index.name = u'网址'
a = counts1_.sort_values(u'点击次数',ascending=False).iloc[:20,:]
a


# In[4]:

#-----* 2 *-----获取网页点击排名数筛选出点击次数>50的有html结尾的网址

b = counts1_.reset_index()
c = b[b[u'点击次数']>50][b[u'网址'].str.contains('/\d+?_*\d+?\.html')]
c.set_index(u'网址',inplace=True)
c.sort_index(inplace = True)
# savetosql(c, 'count355')# 并保存到数据库中
c


# In[5]:

#-----* 3 *-----翻页网页统计，对浏览网页翻页的情况进行统计
# 获取网址中以http://与.html中间的主体部分,即去掉翻页的内容，即去掉尾部"_d"
import re
import numpy as np
pattern = re.compile('http://(.*\d+?)_\w+_\w+\.html$|http://(.*\d+?)_\w+\.html$|http://(.*\w+?).html$',re.S)
c['websitemain'] = np.nan
for i in range(len(c)):
    items = re.findall(pattern, c.index[i])
    if len(items)== 0:
        temp = np.nan
    else:
        for j in items[0]:
            if j !='':
                temp = j
    c.iloc[i,1] = temp
c


# In[6]:

# 获取所有网页主体的网页数
d = c['websitemain'].value_counts()
d = DataFrame(d)
d


# In[7]:

# 统计网页主体出现次数为不少于二次的，即存在翻页的网址
e = d[d['websitemain']>=2]
e.columns=['Times']#记录某网页及子网页出现的此处
e.index.name='websitemain'# 主网页

e['num'] = np.arange(1,len(e)+1) 
f = pd.merge(c,e,left_on='websitemain',right_index=True,how='right')
f.sort_index(inplace=True)
f['per'] = np.nan
f# 相同num的网页是拥有同一网页主体


# In[13]:

# 统计翻子页的点击率与上一页网页点击率的比重（注意：用此处这个方法对网页翻页后序号有10页及以上的合适
def getper(x):
    x.sort_index(inplace=True) #必须先排序将网页
    print x
    for i in range(len(x)-1):
        x.iloc[i+1,-1] = x.iloc[i+1,0]/x.iloc[i,0]
    return x    
        
from __future__ import division

result = DataFrame([]) # 用一个空表格记录值
for i in range(1,f['num'].max()+1):#count36['num'].max()+1
    k= getper(f[f['num'] == i])
    result = pd.concat([result,k])# 每次进行一次操作时
result


# In[15]:

f['Times'].value_counts() # 由统计结果看，只有一个主网址出现过10次及以上，该数据采用上述方法会出问题，因此，在结果中将其剔除后观察剩余数据


# In[16]:

flipPageResult = result[result['Times']<10]
#保存的表名命名格式为“1_3_k此表功能名称”，是此小节生成的第1张表格，功能为flipPageResult：统计翻子页的点击率与上一页网页点击率的比重
flipPageResult.to_excel('1_3_1flipPageResult.xlsx')
flipPageResult


# In[ ]:




# In[ ]:



