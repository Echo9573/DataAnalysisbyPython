# -*- coding:utf-8-*-
import jieba
import sys
seg_list = jieba.cut('我来到北京大学',cut_all = True)
seg_list_tolist = list(seg_list)
for word in seg_list_tolist:
	# sys.stdout.write(word.encode('utf-8')+',')
	sys.stdout.write(word + ',')
