import jieba
from jieba import analyse
from pprint import pprint
def load_stop_words(filename):
from wordcloud import WordCloud
import matplotlib.pyplot as plt
    """ load dictionary file.

    :param filename: The path to the dictionary file
    :return: a list of stop words
    """
    predict = detect_encoding(filename)
    encoding = predict['encoding']
    with io.open(filename, 'r', encoding=encoding, errors='ignore') as f:
        stop_words = set()
        for line in f.readlines():
            stop_words.add(line.strip())
        return stop_words

def filter_stop_words(cut_word_list, stop_words):
        """Filter stop words

        :param cut_word_list: a list of words
        :param stop_words: a list of stop_words
        :return: a list of Filtered words
        """
        seg_list = [
            w for w in cut_word_list if w not in stop_words and w != " "
            ]
        return seg_list

def filter_single_word(words):
    seg_list = [ word for word in words if len(word) > 1]
    return seg_list
# 为了优化结巴的分词效果加载了几个字典
jieba.set_dictionary('dataset/dict/dict.txt.big')
jieba.load_userdict('dataset/dict/custom_words.txt')
jieba.analyse.set_stop_words('dataset/dict/stop_words_filtered.txt')

# 使用上面的 content
keywords = jieba.cut(content)

# 过滤停用词
stop_words = load_stop_words('dataset/dict/stop_words_filtered.txt')
print "stop_words length: %s" % len(stop_words)
keywords = filter_stop_words(keywords, stop_words)
# 过滤长度为1的词，保留长度2以上的词
keywords = filter_single_word(keywords)
words_frequency_dict = dict()

# 统计词频
for word in keywords:
    words_frequency_dict[word] = words_frequency_dict.get(word, 0) + 1
words_frequency = words_frequency_dict.items()
print "words_frequency length: %s" % len(words_frequency)

# 找到词频排前2000的词语
top_n = len(words_frequency) if len(words_frequency) < 2000 else 2000
top_words_frequency = sorted(words_frequency,key=lambda x: x[1],reverse=True)[:top_n]
for word,fre in top_words_frequency[:200]:
    print word, fre


def show_img(wc):
    plt.figure()
    plt.imshow(wc)
    plt.axis("off")
# 实例化，通过font_path传入一个支持中文的字体
wc = WordCloud(font_path=u"AaGuDianKeBenSong-2.ttf",
               max_words=2000,
               width=1920,
               height=1080,
               background_color="black",
               margin=5)

# 1、传入[（key，weight）,...]列表生成词云
wc.generate_from_frequencies(key_words)
# 2、传入"key key key key" 字符串生成词云
# wc.generate(content)

# 保存图片到本地
wc.to_file('result/santi/santi_textrank_filtered(nb_n_nr_ns_a_ad_an_nt_nz_v_d).png')
show_img(wc)
