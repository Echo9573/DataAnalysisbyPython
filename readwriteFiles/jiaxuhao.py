#coding:utf-8
# -*- coding: gbk -*-
"""
Created on Fri Mar 03 14:39:34 2017

@author: Zhu Wen Jing
"""
import re

f = open(r'C:\Users\Zhu Wen Jing\Desktop\PythonStudy\yihangwenzhang.txt','r+')
fil1 = f.readlines()
a = []
for i in range(len(fil1)):
    # a.append('['+str(i)+']'+fil1[i])
    strr=str(i+1).center(2)
    a.append('['+strr+']'+fil1[i])
f.close()

f = open(r'C:\Users\Zhu Wen Jing\Desktop\PythonStudy\xuhao.txt','w')
for i in a:
    f.write(i)
f.close()
#
# print '2————————————————————————'
# pat =r'\n'
# for i in range(len(f1)):
#     f1[i] = re.sub(pat, '',f1[i])
# c = f1
# print '3————————————————————————'
# print c
# for i in range(len(c)/10):
#     c.insert(i*10+i,'\n')
#
# fil = open(r'C:\Users\Zhu Wen Jing\Desktop\PythonStudy\1nonecixing.txt','w')
# for i in c:
#     fil.write(i)
# fil.close()



#
# a1 = []
# b1 = []
# print lines1
# # 此处去除头部end及序号
# print range(lines1/10)
# for i in range(lines1/10):
#     for j in range(10):
#         b1.append(f1[i*10+j%10])
#         print '2————————————————————————'
#     print b1
# print b1
# print len(a1)


#
# c1 = []
# d1 = []
# for i in a1:
#     for j in range(10):
#         c1.extend(i[j])
#     c1.extend('\n')
# #
#
#
# f.close()
# print '2————————————————————————'

# print '3————————————————————————'
# fil = open(r'C:\Users\Zhu Wen Jing\Desktop\PythonStudy\nonecixing.txt','w')
# for i in c:
#     fil.write(i+' ')
# fil.close()




# c1 = set (a1)
# c2 = set (a2)
# fil = open(r'C:\Users\Zhu Wen Jing\Desktop\PythonStudy\WP_Ict_test-WP_Ict_test2.txt','w')
# for i in c1.difference(c2):
#     fil.write(i+' ')
# fil.close()
#
# fil = open(r'C:\Users\Zhu Wen Jing\Desktop\PythonStudy\WP_Ict_test2-WP_Ict_test.txt', 'w')
# for i in c2.difference(c1):
#     fil.write(i+' ')
# fil.close()
#
# fil = open(r'C:\Users\Zhu Wen Jing\Desktop\PythonStudy\WP_Ict_test_WP_Ict_test2.txt', 'w')
# for i in c1.intersection(c2):
#     fil.write(i+' ')
# fil.close()
#
# fil = open(r'C:\Users\Zhu Wen Jing\Desktop\PythonStudy\WP_Ict_test+WP_Ict_test2.txt', 'w')
# for i in c1.union(c2):
#     fil.write(i+' ')
# fil.close()
#
#coding:utf-8