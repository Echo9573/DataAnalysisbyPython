# -*- coding:utf-8 -*-
# Python实现读取目录所有文件的文件名并保存到txt文件代码
# 方法一：使用os.listdir
import os
def ListFilesToTxt(dir,file,wildcard,recursion):
    exts = wildcard.split(" ")
    files = os.listdir(dir)
    for name in files:
        fullname=os.path.join(dir,name)
        if(os.path.isdir(fullname) & recursion):
            ListFilesToTxt(fullname,file,wildcard,recursion)
        else:
            for ext in exts:
                if(name.endswith(ext)):
                    file.write(name + "\n")
                    break
def Test():
  dir="C:/Users/zhuwenjing/Desktop/dairy/2_summerVacation"
  outfile="binaries.txt"
  wildcard = ".txt .exe .dll .lib"

  file = open(outfile,"w")
  if not file:
    print ("cannot open the file %s for writing" % outfile)
  ListFilesToTxt(dir,file,wildcard, 1)
  file.close()

Test()
dir = "C:/Users/zhuwenjing/Desktop/dairy/2_summerVacation"
print os.listdir(dir)


# # 方法2：使用os.walk递归地对目录及子目录处理，每次返回的三项分别为：当前递归的目录，当前递归的目录下的所有子目录，
# # 当前递归的目录下的所有文件。
# import os
# def ListFilesToTxt(dir,file,wildcard,recursion): #recursion控制递归深度，只递归当前目录（*****）
#     exts = wildcard.split(" ")
#     for root, subdirs, files in os.walk(dir):
#         for name in files:
#             for ext in exts:
#                 if(name.endswith(ext)): # (*****)
#                     file.write(name + "\n")
#                     break
#         if(not recursion):
#             break
# def Test():
#   dir=r"C:/Users/zhuwenjing/Desktop/dairy/2_summerVacation"
#   outfile="binaries.txt"
#   wildcard = ".txt .exe .dll .lib"
#
#   file = open(outfile,"w")
#   if not file:
#     print ("cannot open the file %s for writing" % outfile)
#   ListFilesToTxt(dir,file,wildcard, 0)
#
#   file.close()
# Test()
