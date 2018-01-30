# -*- coding:utf-8 -*-
# 目标：将一个文件夹下的所有txt日记写到一个文件中（一行是一天的日记）
# 文件格式是：
# 第1周周报20170226.txt
# 第2周工作计划.txt
# 第2周周报20170305.txt
# 第3周工作计划.txt

import glob
import re
# 采用glob模块匹配出目标文件夹下的所有txt后缀名的文件
txt_filenames = glob.glob('C:/Users/zhuwenjing/Desktop/dairy/3_groupOneDown/*.txt')
print txt_filenames

# 采用re模块匹配出txt文件的文件中的数字
pattern = re.compile("[0-9]+", re.S)
txtname = []
for i in txt_filenames:
    name = re.findall(pattern, i )
    name = map(int, name) # 将列表中的数据类型转成数值型
    txtname.append(name)

# 将文件名和列表中的日期信息进行对应匹配，目的是方便按照日期写入顺序排序
pp = zip(txtname,txt_filenames)
pp = sorted(pp)

# 将每个txt文件中的信息放在一行中，并存储到目标文件中
fileout = open(r'C:\Users\zhuwenjing\Desktop\dairy\3_groupOneDown\AllDiary.txt','w+')
for i in range(len(pp)):
    txt_file = open(pp[i][1], 'r') # 注意：这里直接读取文件名即可，不需要解码成utf-8的格式txt_filenames[i].decode('utf-8')
    buf = txt_file.read()  # the context of txt file saved to buf
    content = buf.replace("\n", " ").strip()
    p = str(pp[i][0]) + ' ' + content # 每行开始加上日期数据
    fileout.write(p)
    fileout.write('\n\n')
    txt_file.close()
fileout.close()

