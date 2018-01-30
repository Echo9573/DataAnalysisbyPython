#coding:utf-8
import re
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
pat ='/.*'
for i in range(len(a1)):
    a1[i] = re.sub(pat, '',a1[i])
c = a1
print '3————————————————————————'
fil = open(r'C:\Users\Zhu Wen Jing\Desktop\PythonStudy\nonecixing.txt','w')
for i in c:
    fil.write(i+' ')
fil.close()