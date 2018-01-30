
# coding: utf-8

# In[1]:


# 原始数据去重
import pandas as pd
inputfile = '1_1my_meidi_jd.txt' # 评论汇总文件
data = pd.read_csv(inputfile, encoding = 'utf-8', header = None) #(***)
data.head()


# In[2]:

l1 = len(data) 
print u'原始数据有%d条' % l1
data = pd.DataFrame(data[0].unique())# (*****)
l2 = len(data)
print u'去重后数据有%d条' % l2
data.to_csv('2_1my_meidi_jd_delduplis.txt', header = False, index = False, encoding='utf-8') # (***)



# In[ ]:



