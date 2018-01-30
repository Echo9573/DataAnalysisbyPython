
# coding: utf-8

# In[1]:


# 分词
import pandas as pd
import jieba # 导入结巴分词包

inputfile1 = u'3_1my_meidi_jd_process_end_负面情感结果.txt' 
inputfile2 = u'3_2my_meidi_jd_process_end_正面情感结果.txt'
data1 = pd.read_csv(inputfile1, encoding = 'utf-8', header = None) #(***)
data2 = pd.read_csv(inputfile2, encoding = 'utf-8', header = None) #(***)

mycut = lambda s: " ".join(jieba.cut(s)) # 自定义简单分词函数
data1 = data1[0].apply(mycut) # 通过广播形式分词，加快速度
data2 = data2[0].apply(mycut) # 通过广播形式分词，加快速度

data1.to_csv(u'4_1my_meidi_jd_process_end_负面情感结果_cut.txt', header = False, index = False, encoding='utf-8') # (***)
data2.to_csv(u'4_2my_meidi_jd_process_end_正面情感结果_cut.txt', header = False, index = False, encoding='utf-8') # (***)



# In[ ]:



