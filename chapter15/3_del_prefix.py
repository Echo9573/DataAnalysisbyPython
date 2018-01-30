
# coding: utf-8

# In[1]:


# 删除前缀
import pandas as pd
# 注意：文件名前必须加'u'，要不然会报错
inputfile1 = u'meidi_jd_process_end_负面情感结果.txt' # 评论汇总文件
inputfile2 = u'meidi_jd_process_end_正面情感结果.txt' # 评论汇总文件


data1 = pd.read_csv(inputfile1, encoding = 'utf-8', header = None) #(***)
data2 = pd.read_csv(inputfile2, encoding = 'utf-8', header = None) #(***)

data1 = pd.DataFrame(data1[0].str.replace('.*?\d+?\\t', '')) # 使用正则表达式替换掉前缀
data2 = pd.DataFrame(data2[0].str.replace('.*?\d+?\\t', '')) # 使用正则表达式替换掉前缀

data1.to_csv(u'3_1my_meidi_jd_process_end_负面情感结果.txt', header = False, index = False, encoding='utf-8') # (***)
data2.to_csv(u'3_2my_meidi_jd_process_end_正面情感结果.txt', header = False, index = False, encoding='utf-8') # (***)



# In[ ]:



