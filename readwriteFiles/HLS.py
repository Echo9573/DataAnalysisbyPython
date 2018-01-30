# -*-coding:utf-8-*-
import re
import jieba
import os
import chardet
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
def savefile(savefile,content):
    fp = open(savefile,'w+')
    fp.write(content)
    fp.close()
def savepic(path):


def readfile(path):
    fp = open(path,'rb')
    content = fp.read()
    content = content.replace("\r\n", "").strip()  # 删除换行和空格
    fp.close()
    return content
def subReplace(line):
    regex = re.compile(ur"[，。、…”“（）《》？_]")
    return regex.sub("",line.decode("utf-8"))
#以下是整个语料库的分词主程序
corpus_path = "train_corpus_small/"
seg_path = "train_corpus_seg/"

catelist = os.listdir(corpus_path) #获取corpus_path下的所有子目录
print catelist
#获取每个目录下的所有文件
for mydir in catelist:
    class_path = corpus_path+mydir+'/'
    seg_dir = seg_path+mydir+'/'
    if not os.path.exists(seg_dir):
        os.makedirs(seg_dir)
    file_list = os.listdir(class_path)
    for file_path in file_list:
        full_name = class_path+file_path
        print full_name
        content = readfile(full_name).strip()
        print chardet.detect(content)
        Con= subReplace(content)
        print Con
        content_seg = jieba.cut(Con)
        print content_seg
        #将处理后的文件保存到分词后预料目录
        savefile(seg_dir+file_path," ".join(content_seg))

print "中文预料分词结束"
def subReplace(line):
    regex = re.compile(ur"[，。、…”“（）《》？_]")
    return regex.sub("",line.decode("utf-8"))
line = "“精确地说，…是市公安局在册的…所有于1983年办理出生登记的男孩的名册。”"
print subReplace(line)
#
# seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
# print("Full Mode: " + "/ ".join(seg_list))  # 全模式
#
# seg_list = jieba.cut("他来到网易杭研大厦。")
# print("Default Mode: " + "/".join(seg_list))
#
# seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造。")  #搜索引擎模式
# print("Search Mode: " + "/".join(seg_list))
#
# seg_list = jieba.cut("李小福是创新办主任也是云计算方面的专家。")
# print("Origin: " + "/".join(seg_list))
#
# print("/".join(jieba.cut("如果放到post中将出错。", HMM = False)))
#
# #利用调节词频使“中”，“将”都能被分出来
# jieba.suggest_freq(("中", "将"), tune = True)
#
# # In[9]:
#
# print("/".join(jieba.cut("如果放到post中将出错。", HMM=False)))
#
# # In[16]:
#
# Original = "/".join(jieba.cut("江州市长江大桥参加了长江大桥的通车仪式。", HMM=False))
# print "Original: " + Original
#
# # In[21]:
#
# jieba.add_word("江大桥", freq=20000, tag=None)
# print "/".join(jieba.cut("江州市长江大桥参加了长江大桥的通车仪式。"))
#
# # In[20]:
# #
# # jieba.load_userdict("C:\\Users\\Zhu Wen Jing\\Desktop\\shizhang.txt")
# # print "Revise: " + "/".join(jieba.cut("江州市长江大桥参加了长江大桥的通车仪式。", HMM=False))
import jieba.posseg as pseg
words = pseg.cut("我爱北京天安门。")
for w in words:
    print("%s %s" %(w.word, w.flag))