import  xml.dom.minidom
import csv
import pandas as pd

# 1. 创建文件对象
f = open('Nlpcc2013Train.csv','a+',encoding='utf-8',newline='')

# 2. 基于文件对象构建 csv写入对象
csv_writer = csv.writer(f)


#打开xml文档
dom = xml.dom.minidom.parse('ExpressionTest.xml')

#得到文档元素对象
root = dom.documentElement
wb=dom.getElementsByTagName('weibo')

for i in range(len(wb)):
    wbi=wb[i]
    sens=wbi.getElementsByTagName('sentence')
    for j in range(len(sens)):
        senj=sens[j]
        if senj.firstChild is None:
            continue
        if senj.hasAttribute('emotion-1-type'):
            em=senj.getAttribute('emotion-1-type')
        else:
            continue
        text=senj.firstChild.data
        csv_writer.writerow([em,text])
        
        
f.close()






