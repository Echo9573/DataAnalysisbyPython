
# coding: utf-8

# In[1]:


# 模型构建
import numpy as np
import pandas as pd
import numpy as np
from pandas import Series,DataFrame
from sqlalchemy import create_engine
import MySQLdb as msd
# 将表格写入数据库里
def savetosql(dataframe,tablename):
    import pandas as pd
    from sqlalchemy import create_engine
    yconnect = create_engine('mysql+mysqldb://root:@127.0.0.1:3306/jing?charset=utf8')  
    pd.io.sql.to_sql(dataframe,tablename, yconnect, schema='jing', if_exists='append')
    
# 读取数据库数据——模型数据1——婚姻数据（16824条记录）
engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/jing?charset=utf8')
data = pd.read_sql('hunyinformodel', engine)# 数据不是很大，不用分块了
data.head()


# In[2]:

#-----* 1 *-----基于物品的协同过滤推荐

def Jaccard(a,b): #自定义杰卡德相似系数函数，仅对0-1矩阵有效
    return 1.0*(a*b).sum() /(a+b-a*b).sum()

class Recommender():
    sim = None # 相似度矩阵
    def similarity(self, x, distance): # 计算相似度矩阵的函数
        y = np.ones((len(x), len(x)))
        for i in range(len(x)):
            for j in range(len(x)):
                y[i,j] = distance(x[i], x[j])
        return y
    
    def fit(self, x, distance = Jaccard): # 训练函数
        self.sim = self.similarity(x, distance)
        return self.sim
    
    def recommend(self, a): # 推荐函数
        return np.dot(self.sim, a) * (1-a)


# In[3]:

len(data['fullURL'].value_counts()) # 4339
len(data['realIP'].value_counts()) # 10333
# 由题意知  网址数 < 用户数--> 建立基于物品的协同过滤推荐


# In[4]:

# 将所有数据转成0-1矩阵
# 大概运行时间是40秒左右
import time
start0 = time.clock()
data.sort_values(by=['realIP','fullURL'],ascending=[True,True],inplace=True)
realIP = data['realIP'].value_counts().index
realIP = np.sort(realIP)
fullURL = data['fullURL'].value_counts().index #
fullURL = np.sort(fullURL)
D = DataFrame([], index = realIP, columns = fullURL )

for i in range(len(data)):
    a = data.iloc[i,0] # 用户名
    b = data.iloc[i,1] # 网址
    D.loc[a,b] = 1 
D.fillna(0,inplace = True)
end0 = time.clock()
usetime0 = end0-start0
print '转成0、1矩阵所花费的时间为'+ str(usetime0) +'s!'#34.5123141125s!

#保存的表名命名格式为“3_1_k此表功能名称”，是本小节生成的第1张表格，功能为zero_one：整个数据集计算得到的0-1矩阵
D.to_csv('3_1_1zero_one.csv')


# In[5]:

D.head(20) #D.shape=10333 rows × 4339 columns


# In[6]:

# 目标：采用十折交叉验证方法验证推荐
# 步骤：解决采用一次验证的方法，再创建十折交叉验证循环（此处只采用了一次具体十折交叉方法见3_2_10-fold cross-validation.py）
# 由于是基于物品（网址）的推荐，所以测试集需包含所有网址（全集），选择0.9*总用户数个用户记录来进行训练模型
# 注意：将数据随机打乱

# 随机打乱数据
# 注意 每次打乱数据，下面的都会改变
df = D.copy()

simpler = np.random.permutation(len(df)) 
df = df.take(simpler)# 打乱数据

train = df.iloc[:int(len(df)*0.9), :]
test = df.iloc[int(len(df)*0.9):, :]

df = df.as_matrix()

df_train = df[:int(len(df)*0.9), :]# 前90%为训练集len(df_train) = 9299
df_test = df[int(len(df)*0.9):, :]# 后10%为测试集len(df_test) = 1034

#由于基于物品的推荐，对于矩阵，根据上面的推荐函数，index为网址，因此需要进行转置
df_train = df_train.T
df_test = df_test.T


# In[7]:

print df_train.shape # (4339L, 9299L)
print df_test.shape # (4339L, 1034L)


# In[8]:

# 建立相似矩阵，训练模型
print df_train.shape # (4339L, 9299L)
import time
start1 = time.clock()
r = Recommender()
sim = r.fit(df_train)# 计算物品的相似度矩阵
end1 = time.clock()

a = DataFrame(sim) # 保存相似度矩阵
usetime1 = end1-start1
print u'建立相似矩阵耗时'+str(usetime1)+'s!'  #1981.60760257s!

print a.shape


# 将所有数据保存
a.index = train.columns
a.columns = train.columns

#保存的表名命名格式为“3_1_k此表功能名称”，是本小节生成的第2张表格，功能为similarityMatrix：计算训练集的相似度矩阵
a.to_csv('3_1_2similarityMatrix.csv')
a.head(20)


# In[9]:

# 使用测试集进行预测
print df_test.shape # (4339L, 1034L)
start2 = time.clock()
result = r.recommend(df_test)
end2 = time.clock()

result1 = DataFrame(result)
usetime2 = end2-start2
print u'推荐函数耗时'+str(usetime2)+'s!'

result1


# In[10]:

# 将推荐结果表格中的对应的网址和用户名对应上
result1.index = test.columns
result1.columns = test.index
#保存的表名命名格式为“3_1_k此表功能名称”，是本小节生成的第3张表格，功能为recommedresult：显示推荐的结果
result1.to_csv('3_1_3recommedresult.csv')
result1


# In[11]:

# 定义展现具体协同推荐结果的函数，K为推荐的个数，recomMatrix为协同过滤算法算出的推荐矩阵的表格化
# type(K):int, type(recomMatrix):DataFrame

def xietong_result(K, recomMatrix ): 
    recomMatrix.fillna(0.0,inplace=True)# 将表格中的空值用0填充
    n = range(1,K+1)
    recommends = ['xietong'+str(y) for y in n]
    currentemp = DataFrame([],index = recomMatrix.columns, columns = recommends)
    for i in range(len(recomMatrix.columns)):
        temp = recomMatrix.sort_values(by = recomMatrix.columns[i], ascending = False)
        k = 0 
        while k < K:
            currentemp.iloc[i,k] = temp.index[k]
            if temp.iloc[k,i] == 0.0:
                currentemp.iloc[i,k:K] = np.nan
                break
            k = k+1

    return currentemp

start3 = time.clock()
xietong_result = xietong_result(3, result1)
end3 = time.clock()
print '按照协同过滤推荐方法为用户推荐3个未浏览过的网址耗时为' + str(end3 - start3)+'s!' #29.4996622053s!

#保存的表名命名格式为“3_1_k此表功能名称”，是本小节生成的第4张表格，功能为xietong_result：显示协同过滤推荐的结果
xietong_result.to_csv('3_1_4xietong_result.csv')

xietong_result # 结果中出现了全空的行，这是冷启动现象


# In[12]:

#-----* 2 *-----------随机推荐

# test = df.iloc[int(len(df)*0.9):, :] #　所有测试数据df此时是矩阵，这样不能用
randata = 1 - df_test # df_test是用户浏览过的网页的矩阵形式，randata则表示是用户未浏览过的网页的矩阵形式
randmatrix = DataFrame(randata, index = test.columns,columns=test.index)#这是用户未浏览过(待推荐）的网页的表格形式

# 定义展现具体Ｒandom随机推荐结果的函数，K为推荐的个数，recomMatrix为用户未浏览过的网页的表格形式
# type(K):int, type(recomMatrix):DataFrame

def rand_recommd(K, recomMatrix):#　
    import random # 注意：这个random是random模块，
    import numpy as np
    
    recomMatrix.fillna(0.0,inplace=True)
    recommends = ['recommed'+str(y) for y in range(1,K+1)]
    currentemp = DataFrame([],index = recomMatrix.columns, columns = recommends)
    
    for i in range(len(recomMatrix.columns)): #len(res.columns)1
        curentcol = recomMatrix.columns[i]
        temp = recomMatrix[curentcol][recomMatrix[curentcol]!=0]
    #     = temp.index[random.randint(0,len(temp))]
        if len(temp) == 0:
            currentemp.iloc[i,:] = np.nan
        elif len(temp) < K:
            r = temp.index.take(np.random.permutation(len(temp))) #注意：这个random是numpy模块的下属模块
            currentemp.iloc[i,:len(r)] = r
        else:
            r = random.sample(temp.index, K)
            currentemp.iloc[i,:] =  r
    return currentemp

start4 = time.clock()
random_result = rand_recommd(3, randmatrix) # 调用随机推荐函数
end4 = time.clock()
print '随机为用户推荐3个未浏览过的网址耗时为' + str(end4 - start4)+'s!' # 2.1900423292s!

#保存的表名命名格式为“3_1_k此表功能名称”，是本小节生成的第5张表格，功能为random_result：显示随机推荐的结果
random_result.to_csv('random_result.csv')

random_result # 结果中出现了全空的行，这是冷启动现象


# In[13]:

#-----* 3 *----- 按照网页浏览热度进行推荐  

# 定义展现具体Popular随机推荐结果的函数，K为推荐的个数，recomMatrix为用户未浏览过的网页的表格形式
# type(K):int, type(recomMatrix):DataFrame

def popular_recommed(K, recomMatrix):
    recomMatrix.fillna(0.0,inplace=True)
    import numpy as np
    recommends = ['recommed'+str(y) for y in range(1,K+1)]
    currentemp = DataFrame([],index = recomMatrix.columns, columns = recommends)

    for i in range(len(recomMatrix.columns)):
        curentcol = recomMatrix.columns[i]
        temp = recomMatrix[curentcol][recomMatrix[curentcol]!=0]
        if len(temp) == 0:
            currentemp.iloc[i,:] = np.nan
        elif len(temp) < K:
            r = temp.index #注意：这个random是numpy模块的下属模块
            currentemp.iloc[i,:len(r)] = r
        else:
            r = temp.index[:K]
            currentemp.iloc[i,:] =  r

    return currentemp  



# In[14]:

# 确定用户未浏览的网页（可推荐的）的数据表格
TEST = 1-df_test
test2 = DataFrame(TEST, index = test.columns, columns=test.index)
print test2.head()
print test2.shape 

# 确定网页浏览热度排名：
hotPopular = data['fullURL'].value_counts()
hotPopular = pd.DataFrame(hotPopular)
print hotPopular.head()
print hotPopular.shape 

# 按照流行度对可推荐的所有网址排序
test3 = test2.reset_index()
list_custom = list(hotPopular.index)
test3['index'] = test3['index'].astype('category')
test3['index'].cat.reorder_categories(list_custom, inplace=True)
test3.sort_values('index',inplace = True)
test3.set_index ('index', inplace = True)
print test3.head()
print test3.shape 


# 按照流行度为用户推荐3个未浏览过的网址
recomMatrix = test3
start5 = time.clock()
popular_result = popular_recommed(3, recomMatrix)
end5 = time.clock()
print '按照流行度为用户推荐3个未浏览过的网址耗时为' + str(end5 - start5)+'s!'#7.70043007471s!

#保存的表名命名格式为“3_1_k此表功能名称”，是本小节生成的第6张表格，功能为popular_result：显示按流行度推荐的结果
popular_result.to_csv('3_1_6popular_result.csv')

popular_result


# In[ ]:




# In[ ]:



