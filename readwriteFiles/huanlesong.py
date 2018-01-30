# -*-coding:utf-8-*-
import re
import sys
reload(sys)
sys.setdefultencoding('utf-8')
f = open(r'C:\Users\Zhu Wen Jing\Desktop\PythonStudy\HLS3.txt', 'r')

f1 = f.readlines()  # f1是一个列表类型
lines1 = len(f1)

pat =r'\n'
for i in range(len(f1)):
    f1[i] = re.sub(pat, '',f1[i])

sep = ''
fline = sep.join(f1)
#print fline
f2= fline.replace('第一章','第一章\n')
f2 = fline.split('第一章')
#print type(fline)


#print '3————————————————————————'
del f2[0]
#print f2
sep2 = '\n'
f3 = sep2.join(f2)
#print len(f3)
f.close()
fil = open(r'C:\Users\Zhu Wen Jing\Desktop\mytest1.txt','w')
for i in f3:
    fil.write(i)
fil.close()

f = open(r'C:\Users\Zhu Wen Jing\Desktop\mytest1.txt','r+')
fil1 = f.readlines()
a = []
for i in range(len(fil1)):
    a.append('【'+str(2)+'】'+fil1[i]+'\n')
    #strr=str(i+1).center(2)
    #a.append('['+strr+']'+fil1[i])
f.close()

f = open(r'C:\Users\Zhu Wen Jing\Desktop\PythonStudy\result_HLS3.txt','w')
for i in a:
    f.write(i)
f.close()