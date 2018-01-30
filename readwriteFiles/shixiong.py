# -*- coding: utf-8 -*-
"""
Created on Fri Mar 03 17:03:25 2017

@author: Zhu Wen Jing
"""

import codecs
#
#with open('xxx.txt') as f:
#
#
#for line in f:
#    print(f.read()) 
def main():
    with codecs.open(r'C:\Users\Zhu Wen Jing\Desktop\PythonStudy\WP_Ict_test.txt',encoding='gbk') as f:
        for i in f:
            print i

if __name__=='__main__':
    main()
