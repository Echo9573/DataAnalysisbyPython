# -*- coding:utf-8 -*-
# 目标：将一个文件夹下的所有txt日记写到一个文件中（一行是一天的日记）
# 文件格式是：
# 20170711.txt
# 20170715.txt
# 20170717.txt

import glob
import re
# 采用glob模块匹配出目标文件夹下的所有txt后缀名的文件
txt_filenames = glob.glob('C:/Users/zhuwenjing/Desktop/dairy/*.txt')
print txt_filenames

# 采用re模块匹配出txt文件的文件名称
pattern = re.compile("\\\(.*?)\.txt", re.S)
txtname = []
for i in txt_filenames:
    name = re.findall(pattern, i )
    txtname.append(name[0])
print txtname

# 将每个txt文件中的信息放在一行中，并存储到目标文件中
fileout = open(r'C:/Users/zhuwenjing/Desktop/dairy/AllDiary.txt','w+')
for i in range(len(txt_filenames)):
    txt_file = open(txt_filenames[i], 'r') # 可以转码成txt_filenames[i].decode('utf-8')，也可以不转码
    buf = txt_file.read()  # the context of txt file saved to buf
    content = buf.replace("\n", " ").strip()
    p = txtname[i] + ' ' + content
    fileout.write(p)
    fileout.write('\n\n')
    txt_file.close()
fileout.close()
