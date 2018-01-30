
# coding: utf-8

# In[1]:


# 数据变换
import pandas as pd
import numpy as np
from pandas import Series,DataFrame
from sqlalchemy import create_engine
import MySQLdb as msd
# 先自定义函数将表格写入数据库里，以备操作过程中有些数据要写入数据库
def savetosql(dataframe,tablename):
    import pandas as pd
    from sqlalchemy import create_engine
    yconnect = create_engine('mysql+mysqldb://root:@127.0.0.1:3306/jing?charset=utf8')  
    pd.io.sql.to_sql(dataframe,tablename, yconnect, schema='jing', if_exists='append')  


# In[2]:

#-----* 1 *-----识别翻页的网址并且删除重复（用户ID和处理后的网址相同）的记录

# 读取数据库数据
engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/jing?charset=utf8')
sql = pd.read_sql('cleaned_three', engine, chunksize = 10000)

l0 = 0
l1 = 0
l2 = 0
for i in sql:
    d = i.copy()
    # 获取所有记录的个数
    temp0 = len(d)
    l0 = l0 + temp0
    
    # 获取类似于http://www.lawtime.cn***/2007020619634_2.html格式的记录的个数
    # 匹配1 易知，匹配1一定包含匹配2
    x1 = d[d['fullURL'].str.contains('_\d{0,2}.html')]
    temp1 = len(x1)
    l1 = l1 + temp1    

    # 匹配2
    # 获取类似于http://www.lawtime.cn***/29_1_p3.html格式的记录的个数
    x2 = d[d['fullURL'].str.contains('_\d{0,2}_\w{0,2}.html')]
    temp2 = len(x2)
    l2 = l2 + temp2
    
    x1.to_sql('l1', engine, index=False, if_exists = 'append') # 保存
    x2.to_sql('l2', engine, index=False, if_exists = 'append') # 保存

print l0,l1,l2


# In[3]:

# 注意：在内部循环中，容易删除不完整，所以需要进行全部读取二次筛选删除
# 【初步筛选】
# 读取数据库数据
engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/jing?charset=utf8')
sql = pd.read_sql('cleaned_three', engine, chunksize = 10000)
l4 = 0
for i in sql:
    d = i.copy()

    # 注意！！！替换1和替换2的顺序不能颠倒，否则删除不完整
    # 替换1 将类似于http://www.lawtime.cn***/29_1_p3.html下划线后面部分"_1_p3"去掉，规范为标准网址 
    d['fullURL'] = d['fullURL'].str.replace('_\d{0,2}_\w{0,2}.html','.html')#这部分网址有　9260　个
    
    # 替换2 将类似于http://www.lawtime.cn***/2007020619634_2.html下划线后面部分"_2"去掉，规范为标准网址
    d['fullURL'] = d['fullURL'].str.replace('_\d{0,2}.html','.html') #这部分网址有　55455-9260 = 46195 个
    
    d = d.drop_duplicates(['fullURL','userID']) # 删除重复记录(删除有相同网址和相同用户ID的)【不完整】因为不同的数据块中依然有重复数据
    temp = len(d)
    l4 = l4 + temp
    d.to_sql('changed_1', engine, index=False, if_exists = 'append') # 保存

print l4 # 547608


# In[4]:

# 【二次筛选】
# 删除重复记录
# 读取数据库数据（基于操作2之后）
engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/jing?charset=utf8')
sql = pd.read_sql('changed_five', engine, chunksize = 10000)

def dropduplicate(i): 
    j = i[['realIP','fullURL','pageTitle','userID','timestamp_format']].copy()
    return j

counts1 = [dropduplicate(i) for i in sql]
counts1 = pd.concat(counts1)
print len(counts1)# 547608
a = counts1.drop_duplicates(['fullURL','userID'])
print len(a)# 528166
savetosql(a, 'dataChange')


# In[5]:

# 查看经过数据变换替换后的数据是否替换干净
# 读取数据库数据 
engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/jing?charset=utf8')
sql = pd.read_sql('changed_six', engine, chunksize = 10000)

l0 = 0
l1 = 0
l2 = 0
for i in sql:
    d = i.copy()
    # 获取所有记录的个数
    temp0 = len(d)
    l0 = l0 + temp0
    
    # 获取类似于http://www.lawtime.cn***/2007020619634_2.html格式的记录的个数
    # 匹配1 易知，匹配1一定包含匹配2
    x1 = d[d['fullURL'].str.contains('_\d{0,2}.html')]
    temp1 = len(x1)
    l1 = l1 + temp1    

    # 匹配2
    # 获取类似于http://www.lawtime.cn***/29_1_p3.html格式的记录的个数
    x2 = d[d['fullURL'].str.contains('_\d{0,2}_\w{0,2}.html')]
    temp2 = len(x2)
    l2 = l2 + temp2

print l0,l1,l2# 528166 0 0表示已经删除成功


# In[6]:

#-----* 2 *-----网址正确分类:手动分析咨询类别和知识类别的网址


# 读取数据库数据 
engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/jing?charset=utf8')
sql = pd.read_sql('changed_six', engine, chunksize = 10000)

def countzhishi(i):
    j = i[['fullURL']].copy()
    j['type'] = 'else'
    j['type'][j['fullURL'].str.contains('(info)|(faguizt)')] = 'zhishi'
    j['type'][j['fullURL'].str.contains('(ask)|(askzt)')] = 'zixun'
    
    return j
counts2 = [countzhishi(i) for i in sql]
counts2 = pd.concat(counts2)
counts2['type'].value_counts()


# In[7]:

# 统计各个类别占比
a = counts2['type'].value_counts()
b = DataFrame(a)
b.columns = ['num']
b.index.name = 'type'
b['per'] = b['num']/b['num'].sum()*100
b


# In[8]:

# 第一步 *: 手动分析知识类别的网址，得出知识类别下的二级类别有哪些
c = counts2[counts2['type']=='zhishi']

d = c[c['fullURL'].str.contains('info')]
print len(d) # 102140
d['iszsk'] = 'else' # 结果显示是空  
d['iszsk'][d['fullURL'].str.contains('info')] = 'infoelsezsk' # 102032
d['iszsk'][d['fullURL'].str.contains('zhishiku')] = 'zsk' # 108
d['iszsk'].value_counts()  
# 由结果可知，除了‘info'和’zhishifku'没有其他类型，且 【info类型（不包含zhishiku)：infoelsezsk】和【包含zhishiku：zsk】类型无相交的部分。
# 因此分析知识类别下的二级类型时，需要分两部分考虑，求每部分的类别，再求并集，即为所有二级类型


# In[9]:

# 第二步 *用正则表达式匹配出网址中二级类别
# 方法：用上面已经处理的'iszsk'列分成两种类别的网址，分别使用正则表达式进行匹配
# 缺点：太慢了！！！！！！！！！！！！！！
import re
# 对于http://www.lawtime.cn/info/jiaotong/jtsgcl/2011070996791.html类型的网址进行这样匹配,获取二级类别名称"jiaotong"
pattern = re.compile('/info/(.*?)/',re.S)
e = d[d['iszsk'] == 'infoelsezsk']
for i in range(len(e)):
    e.iloc[i,2] = re.findall(pattern, e.iloc[i,0])[0]
print e.head()

# 对于http://www.lawtime.cn/zhishiku/laodong/info/***.html类型的网址进行这样匹配,获取二级类别名称"laodong"
# 由于还有一类是http://www.lawtime.cn/zhishiku/laodong/***.html，所以使用'zhishiku/(.*?)/'进行匹配
pattern1 = re.compile('zhishiku/(.*?)/',re.S)
f = d[d['iszsk'] == 'zsk']
for i in range(len(f)):
#     print i 
    f.iloc[i,2] = re.findall(pattern1, f.iloc[i,0])[0]
print f.head()


# In[ ]:




# In[10]:

# 第三步 *将列名重命名
e.columns = ['fullURL', 'type1', 'type2']
print e.head()

f.columns = ['fullURL', 'type1', 'type2']
print f.head()

# 将两类处理过二级类别的记录合并，求二级类别的交集
g = pd.concat([e,f])
h = g['type2'].value_counts()

# 求两类网址中的二级类别数，由结果可知，两类网址的二级类别的集合的并集满足所需条件
len(e['type2'].value_counts()) # 66
len(f['type2'].value_counts()) # 31
len(g['type2'].value_counts()) # 69

print h.head()

print h.index # 列出知识类别下的所有的二级类别


# In[11]:

#保存的表名命名格式为“2_2_k此表功能名称”，此表表示生成的第1张表格，功能为Type2nums：
h.to_excel('2_2_1Type2nums.xlsx')
# 将知识类别中不包含zhishiku的提取出来保存到数据库
savetosql(e,'infoelsezsk')


# In[13]:

# 第四步 *将二级类别分别存储到数据库中
# detailtypes = h.index
# for i in range(len(detailtypes)):
#     x = g[g['type2'] == h.index[i]]
#     savetosql(x,h.index[i])


# In[14]:

# 第五步 *用正则表达式匹配出网址中三级类别-----------
# 注意：由coun7中的记录可知，在zhishiku中不存在三级类别:#http://www.lawtime.cn/zhishiku/laodong/info/2108.html
e.head()


# In[17]:

# 复制e的备份进行处理，避免操作中改变了数据
q = e.copy()
q['type3'] = np.nan
resultype3 = DataFrame([],columns=q.columns)
for i in range(len(h.index)):
    pattern2 = re.compile('/info/'+h.index[i]+'/(.*?)/',re.S)
    current = q[q['type2'] == h.index[i]]
    print current.head()
    for j in range(len(current)):
        findresult = re.findall(pattern2, current.iloc[j,0])
        if findresult == []: # 若匹配结果是空，则将空值进行赋值给三级类别
            current.iloc[j,3] = np.nan
        else:
            current.iloc[j,3] = findresult[0]
    resultype3 = pd.concat([resultype3,current])# 将处理后的数据拼接
resultype3.head()


# In[27]:

resultype3.set_index('fullURL',inplace=True)
resultype3.head(10)


# In[28]:

savetosql(resultype3,'resultype3')


# In[29]:

# 统计婚姻类下面的三级类别的数目
j = resultype3[resultype3['type2'] == 'hunyin']['type3'].value_counts()
print len(j) # 145
j.head()


# In[55]:

# 第六步 *目标：将类别3按照每类降序排列，然后保存
# 方式1
Type3nums = resultype3.pivot_table(index = ['type2','type3'], aggfunc = 'count')
# 方式2: Type3nums = resultype3.groupby([resultype3['type2'],resultype3['type3']]).count()
r = Type3nums.reset_index().sort_values(by=['type2','type1'],ascending=[True,False])
r.set_index(['type2','type3'],inplace = True)
r.to_excel('Type3nums.xlsx')
r


# In[ ]:




# In[ ]:

#-----* 3 *-----获取后续建模需要的数据  咨询（ask）和婚姻（hunyin）数据
#-----------------------------
# 将满足需求的存到数据库中去
# 方法一：
# 读取数据库数据 
engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/jing?charset=utf8')
sql = pd.read_sql('changed_six', engine, chunksize = 10000)
l1 = 0
l2 = 0
for i in sql:
    zixun = i[['userID','fullURL']][i['fullURL'].str.contains('(ask)|(askzt)')].copy()
    l1 = len(zixun) + l1
    hunyin = i[['userID','fullURL']][i['fullURL'].str.contains('hunyin')].copy()    
    l2 = len(hunyin) + l2
    zixun.to_sql('zixunformodel', engine, index=False,if_exists = 'append')
    hunyin.to_sql('hunyinformodel', engine, index=False,if_exists = 'append')
print l1,l2 # 393185 16982



# 方法二：
m = counts2[counts2['type'] == 'zixun']
n =counts2[counts2['fullURL'].str.contains('hunyin')]
p = m[m['fullURL'].str.contains('hunyin')]
p # 结果为空，可知，包含zixun的页面中不包含hunyin，两者没有交集
savetosql(m,'zixun')
savetosql(n,'hunyin')


# In[ ]:



