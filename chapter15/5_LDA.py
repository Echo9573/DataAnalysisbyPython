
# coding: utf-8

# In[1]:


# LDA算法实现
# 方法：在分好词的正面评价、负面评价以及过滤用的停用词表上进行，使用Gensim库完成LDA分析代码
import pandas as pd

# 参数初始化
inputfile1 = u'4_1my_meidi_jd_process_end_负面情感结果_cut.txt' 
inputfile2 = u'4_2my_meidi_jd_process_end_正面情感结果_cut.txt'
inputfile3 = 'stoplist.txt' # 停用词表

data1 = pd.read_csv(inputfile1, encoding = 'utf-8', header = None) #(***)
data2 = pd.read_csv(inputfile2, encoding = 'utf-8', header = None) #(***)
stop = pd.read_csv(inputfile3, encoding = 'utf-8', sep = 'tipdm', header = None) #(***)
# sep 设置分割词， 由于csv默认以半角逗号为分割词，而该词恰好在停用词表中，因此会导致读取出错
# 所以，解决方法是手动设置一个不存在的分割词，如tipdm
print data1.head()
print data2.head()
print stop.head()


# In[2]:

stop = [' ', ''] +list(stop[0]) # pandas自动过滤了空格符，所以手动将其加入

data1 [1] = data1[0].apply(lambda s: s.split(' ')) # 定义一个分隔函数，用apply广播
data1 [2] = data1[1].apply(lambda x: [i for i in x if i not in stop]) # 逐词判断是否是停用词

data2 [1] = data2[0].apply(lambda s: s.split(' ')) # 定义一个分隔函数，用apply广播
data2 [2] = data2[1].apply(lambda x: [i for i in x if i not in stop]) # 逐词判断是否是停用词
print data1.head()
print data2.head()


# In[3]:

from gensim import corpora, models


# In[4]:

# 负面主题分析
data1_dict = corpora.Dictionary(data1[2]) # 建立词典
data1_corpus = [data1_dict.doc2bow(i) for i in data1[2]] # 建立语料库

data1_LDA = models.LdaModel(data1_corpus, num_topics =3, id2word = data1_dict) # LDA训练模型
for i in range(3):
    data1_LDA.print_topic(i)# 输出每个主题


# In[5]:

# 正面主题分析
data2_dict = corpora.Dictionary(data2[2]) # 建立词典
data2_corpus = [data2_dict.doc2bow(i) for i in data2[2]] # 建立语料库

data2_LDA = models.LdaModel(data2_corpus, num_topics =3, id2word = data2_dict) # LDA训练模型
for i in range(3):
    data2_LDA.print_topic(i)# 输出每个主题


# In[8]:

data1_LDA.print_topic(0)


# In[9]:

data2_LDA.print_topic(1)


# In[ ]:



