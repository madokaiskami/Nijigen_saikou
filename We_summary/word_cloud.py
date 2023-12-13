import jieba
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def trans_ch(txt):
  words = jieba.lcut(txt)
  newtxt = ''.join(words)
  return newtxt


f = open('example.txt','r',encoding = 'utf-8')     #将你的文本文件名与此句的'example.txt'替换
txt = f.read()
f.close
txt = trans_ch(txt)
mask = np.array(Image.open("Image.png"))               #将你的背景图片名与此句的"Image.png"替换
wordcloud = WordCloud(background_color="white",\
                      width = 800,\
                      height = 600,\
                      max_words = 200,\
                      max_font_size = 80,\
                      mask = mask,\
                      contour_width = 4,\
                      contour_color = 'steelblue',\
                        font_path =  "msyh.ttf"
                      ).generate(txt)
wordcloud.to_file('love_词云图.png')

