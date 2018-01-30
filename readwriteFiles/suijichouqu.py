#coding:utf-8

import re
import random

#给定初始文档file1和输出文档file2，以及抽取的个数num
def suijichouqu(file1, file2, num):

    f = open(file1,'r+')
    f1 = f.readlines()
    r1 =random.sample(range(0,len(f1)),num)
    f2=[]
    for i in range(num):
        f2.append(f1[r1[i]])
    f.close()
    f = open(file2,'w')
    for i in f2:
        f.write(i)
    f.close()
f1='C:\Users\Zhu Wen Jing\Desktop\PythonStudy\yihangwenzhang.txt'
f2='C:\Users\Zhu Wen Jing\Desktop\PythonStudy\suiji.txt'

if __name__=='__main__':
    suijichouqu(f1, f2, 300)
