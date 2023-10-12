import chardet
import re
import pandas as pd

def load_csv(filename):
    predict = detect_encoding(filename)
    encoding = predict['encoding']
    try:
        with open(filename,'r',encoding=encoding,errors='ignore') as f:
            # 过滤特殊符号
            text = re.sub(r'\W+', ' ', f.read(100), flags=re.U)
            return ''.join(text)
