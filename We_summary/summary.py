#coding:utf-8
import nltk
import jieba
import numpy



#分句
def sent_tokenizer(texts):
    start=0
    i=0#每个字符的位置
    sentences=[]
    punt_list=',.!?:;~，。！？：；～'#标点符号

    for text in texts:#遍历每一个字符
        if text in punt_list and token not in punt_list: #检查标点符号下一个字符是否还是标点
            sentences.append(texts[start:i+1])#当前标点符号位置
            start=i+1#start标记到下一句的开头
            i+=1
        else:
            i+=1#若不是标点符号，则字符位置继续前移
            token=list(texts[start:i+2]).pop()#取下一个字符.pop是删除最后一个
    if start<len(texts):
        sentences.append(texts[start:])#这是为了处理文本末尾没有标点符号的情况
    return sentences

#对停用词加载
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords

#对句子打分
def score_sentences(sentences,topn_words):#参数 sentences：文本组（分好句的文本，topn_words：高频词组
    scores=[]
    sentence_idx=-1#初始句子索引标号-1
    for s in [list(jieba.cut(s)) for s in sentences]:# 遍历每一个分句，这里的每个分句是 分词数组 分句1类似 ['花', '果园', '中央商务区', 'F4', '栋楼', 'B33', '城', '，']
        sentence_idx+=1 #句子索引+1。。0表示第一个句子
        word_idx=[]#存放关键词在分句中的索引位置.得到结果类似：[1, 2, 3, 4, 5]，[0, 1]，[0, 1, 2, 4, 5, 7]..
        for w in topn_words:#遍历每一个高频词
            try:
                word_idx.append(s.index(w))#关键词出现在该分句子中的索引位置
            except ValueError:#w不在句子中
                pass
        word_idx.sort()
        if len(word_idx)==0:
            continue

        #对于两个连续的单词，利用单词位置索引，通过距离阀值计算族
        clusters=[] #存放的是几个cluster。类似[[0, 1, 2], [4, 5], [7]]
        cluster=[word_idx[0]] #存放的是一个类别（簇） 类似[0, 1, 2]
        i=1
        while i<len(word_idx):#遍历 当前分句中的高频词
            CLUSTER_THRESHOLD=2#举例阈值我设为2
            if word_idx[i]-word_idx[i-1]<CLUSTER_THRESHOLD:#如果当前高频词索引 与前一个高频词索引相差小于3，
                cluster.append(word_idx[i])#则认为是一类
            else:
                clusters.append(cluster[:])#将当前类别添加进clusters=[]
                cluster=[word_idx[i]] #新的类别
            i+=1
        clusters.append(cluster)

        #对每个族打分，每个族类的最大分数是对句子的打分
        max_cluster_score=0
        for c in clusters:#遍历每一个簇
            significant_words_in_cluster=len(c)#当前簇 的高频词个数
            total_words_in_cluster=c[-1]-c[0]+1#当前簇里 最后一个高频词 与第一个的距离
            score=1.0*significant_words_in_cluster*significant_words_in_cluster/total_words_in_cluster
            if score>max_cluster_score:
                max_cluster_score=score
        scores.append((sentence_idx,max_cluster_score))#存放当前分句的最大簇（说明下，一个分解可能有几个簇） 存放格式（分句索引，分解最大簇得分）
    return scores;

#结果输出
def results(texts,topn_wordnum,n):#texts 文本，topn_wordnum高频词个数,为返回几个句子
    stopwords = stopwordslist("/content/stopwordslist.txt")#加载停用词
    sentence = sent_tokenizer(texts)  # 分句
    words = [w for sentence in sentence for w in jieba.cut(sentence) if w not in stopwords if
             len(w) > 1 and w != '\t']  # 词语，非单词词，同时非符号
    wordfre = nltk.FreqDist(words)  # 统计词频
    topn_words = [w[0] for w in sorted(wordfre.items(), key=lambda d: d[1], reverse=True)][:topn_wordnum]  # 取出词频最高的topn_wordnum个单词

    scored_sentences = score_sentences(sentence, topn_words)#给分句打分

    # 1,利用均值和标准差过滤非重要句子
    avg = numpy.mean([s[1] for s in scored_sentences])  # 均值
    std = numpy.std([s[1] for s in scored_sentences])  # 标准差
    mean_scored = [(sent_idx, score) for (sent_idx, score) in scored_sentences if
                   score > (avg + 0.5 * std)]  # sent_idx 分句标号，score得分

    # 2，返回top n句子
    top_n_scored = sorted(scored_sentences, key=lambda s: s[1])[-n:]  # 对得分进行排序，取出n个句子
    top_n_scored = sorted(top_n_scored, key=lambda s: s[0])  # 对得分最高的几个分句，进行分句位置排序
    c = dict(mean_scoredsenteces=[sentence[idx] for (idx, score) in mean_scored])
    c1=dict(topnsenteces=[sentence[idx] for (idx, score) in top_n_scored])
    return c,c1

if __name__=='__main__':
    filename = str(input('Please enter the filename：'))
    df = pd.read_csv(filename)
    message = []
    [wmin,wmax] = input("Range of the fisrt sentence and the last sentence，please use　"," to split:").split(",")
    for msg in range(int(wmin),int(wmax)):
      message.append(str(df['Message'][msg]))
    texts = str(message)
    topn_wordnum=int(input('Please enter the number of high-frequency words：'))
    n=int(input('Please enter the number of sentences to be returned：'))
    c,c1=results(texts,topn_wordnum,n)
    with open("./example.txt", 'w') as f:
        f.writelines(c['mean_scoredsenteces'])
        f.close()
    print(c)
    print(c1)
