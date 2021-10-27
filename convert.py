# 将xml文件整体转为简体中文

from opencc import OpenCC
 
INPUT = open('../data/wiki.xml',encoding='utf-8')
a = INPUT.read()
b = OpenCC('t2s').convert(a)
OUTPUT = open('../data/wiki_simple.xml','w',encoding='utf-8')
OUTPUT.write(b)
OUTPUT.close()