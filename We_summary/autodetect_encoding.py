import chardet
import re
import pandas as pd

def detect_encoding(filename):
    with open(filename,'rb') as f:
      predict = chardet.detect(f.read(100))
    if predict['confidence'] < 0.8:
      print(predict)
    else:
      print("auto detect encodings fail:%s" % filename )
    return predict

if __name__=='__main__':
    filename = str(input('请输入文件名：'))
    predict = detect_encoding(filename)
