
# coding: utf-8


#模型构建
#使用K-means聚类算法分类并分析每类的特征
import pandas as pd
from pandas import DataFrame,Series
from sklearn.cluster import KMeans #导入K均值聚类算法
k = 5 # 聚为5类
d3 = pd.read_excel('sjbzh.xlsx')

#调用k-means算法，进行聚类分析
kmodel = KMeans(n_clusters=k, n_jobs=4)# n_job是并行数，一般等于CPU数较好
kmodel.fit(d3)


labels = kmodel.labels_#查看各样本类别
demo = DataFrame(labels,columns=['numbers'])
demo1= DataFrame(kmodel.cluster_centers_, columns=d3.columns) # 保存聚类中心
demo2= demo['numbers'].value_counts() # 确定各个类的数目

demo4 = pd.concat([demo2,demo1],axis=1)
demo4.index.name='labels'
demo4.to_excel('kmeansresults.xlsx')


print kmodel.cluster_centers_#查看聚类中心
print kmodel.labels_#查看各样本类别



#画雷达图 客户群特征分析图
subset = demo1.copy()
subset = subset.round(3)
subset.to_excel('testradar.xlsx')

data = demo1.as_matrix()
from radar1 import drawRader
title = 'RadarPicture'
rgrids = [0.5, 1, 1.5, 2, 2.5]
itemnames = ['ZL','ZR','ZF','ZM','ZC']
labels = list('abcde')
drawRader(itemnames=itemnames,data=data,title=title,labels=labels, saveas = '2.jpg',rgrids=rgrids)

