#coding:utf-8
# -*- coding: gbk -*-
"""
Created on Fri Mar 03 14:39:34 2017

@author: Zhu Wen Jing
"""
import re

# import chardet
# import re
f = open(r'C:\Users\Zhu Wen Jing\Desktop\PythonStudy\train.txt', 'r')

f1 = f.readlines()  # f1是一个列表类型
lines1 = len(f1)
print '1————————————————————————'
# print f1
pat =r'\n'
for i in range(len(f1)):
    f1[i] = re.sub(pat, '',f1[i])
print '2————————————————————————'
# print f1
print len(f1)
sep = ''
fline = sep.join(f1)
# print fline
f2 = fline.replace('1/1', '\n//dd')

f3 = f2.split('//dd')
del f3[0]
print len(f3)
f4 = []
a = []
for i in range(len(f3)):
    strr=str(i+1).center(2)
    f4.append('【'+strr+'】'+f3[i])
f.close()
# for i in range(len(f3)):
#     print f3[i]% i
# print f4
# print '3————————————————————————'
# del f2[0]
# print f2
#
# sep2 = '\n'
# f3 = sep2.join(f2)
# print len(f3)

# pat =r'\n'
# for i in range(len(f2)):
#     f2[i] = re.sub(pat, '',f2[i])
# print '3————————————————————————'

# print f2

fil = open(r'C:\Users\Zhu Wen Jing\Desktop\PythonStudy\yihangwenzhang1.txt','w')
for i in f4:
    fil.write(i)
fil.close()

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
