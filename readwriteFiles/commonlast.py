#coding:utf-8
# -*- coding: gbk -*-
"""
Created on Fri Mar 03 14:39:34 2017

@author: Zhu Wen Jing
"""
import re

# import chardet

f = open(r'C:\Users\Zhu Wen Jing\Desktop\PythonStudy\WP_Ict_test.txt', 'r')

f1 = f.readlines()  # f1是一个列表类型
lines1 = len(f1)
# print f1
print '1————————————————————————'
a1 = []
b1 = []

# 此处去除头部end及序号
for i in range(lines1):
    b1 = f1[i].split()
    del b1[0]
    a1.extend(b1)
f.close()
print a1
print '2————————————————————————'
mm1 = str(a1)

# 统计该文本中wiki词性的词的个数
print mm1.count('/wiki')

f = open(r'C:\Users\Zhu Wen Jing\Desktop\PythonStudy\WP_Ict_test2.txt', 'r')

f2 = f.readlines()  # f1是一个列表类型
lines2 = len(f2)
# print f2
print '1————————————————————————'
a2 = []
b2 = []

# 此处去除头部end及序号
for i in range(lines2):
    b2 = f2[i].split()
    del b2[0]
    a2.extend(b2)
f.close()
print a2
print '2————————————————————————'
mm2 = str(a2)
# 统计该文本中wiki词性的词的个数
print mm2.count('/wiki')

c1 = set (a1)
c2 = set (a2)
print len(c1.difference(c2))
print len(c1.intersection(c2))
print len(c1-c2)
print len(c2.difference(c1))
print len(c2.intersection(c1))
print len(c2-c1)

fil = open(r'C:\Users\Zhu Wen Jing\Desktop\PythonStudy\WP_Ict_test-WP_Ict_test2.txt','w')
for i in c1.difference(c2):
    fil.write(i+' ')
fil.close()

fil = open(r'C:\Users\Zhu Wen Jing\Desktop\PythonStudy\WP_Ict_test2-WP_Ict_test.txt', 'w')
for i in c2.difference(c1):
    fil.write(i+' ')
fil.close()

fil = open(r'C:\Users\Zhu Wen Jing\Desktop\PythonStudy\WP_Ict_test_WP_Ict_test2.txt', 'w')
for i in c1.intersection(c2):
    fil.write(i+' ')
fil.close()

fil = open(r'C:\Users\Zhu Wen Jing\Desktop\PythonStudy\WP_Ict_test+WP_Ict_test2.txt', 'w')
for i in c1.union(c2):
    fil.write(i+' ')
fil.close()

