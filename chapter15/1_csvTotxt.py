
# coding: utf-8

# In[1]:


import pandas as pd
inputfile = 'huizong.csv' # 评论汇总文件
data = pd.read_csv(inputfile, encoding = 'utf-8')
data.head()


# In[2]:

result = data[[u'评论']][data[u'品牌'] == u'美的']
result.info()


# In[3]:

result.head()


# In[4]:

# 必须导入下面这个包，要不然会报错'ascii' codec can't encode characters in position
# Python在安装时，默认的编码是ascii，当程序中出现非ascii编码时，python的处理常常会报这样的错
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
result.to_csv('1_1my_meidi_jd.txt', index = False, header = False) # 将评论提取后保存到txt中，不要索引，不要列名（***）


# In[ ]:



