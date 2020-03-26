from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import jieba
import xlrd
import jieba.analyse
from gensim import corpora, models, similarities

wordsdata=[]
txtName = "commentsWord.txt"
f=open(txtName, "a+")
data = xlrd.open_workbook('comments.xlsx','r', encoding_override='utf-8')
table = data.sheets()[0]
nrows = table.nrows
ncols=table.ncols
for i in range(1, ncols):
    for j in range(1, nrows):
        result = table.row_values(j)[i]  # 第j行第i列的值取出赋给result
        jieba.load_userdict('dict.txt')
        b = jieba.analyse.extract_tags(result, topK=20, withWeight=False, allowPOS=())
        l = len(b)
        for k in range(l):
            f.write(b[k]+" ")
            # print(b[k]+" ")
fr = open('commentsWord.txt', 'r', encoding='gbk')
train = []
for line in fr.readlines():
    line = [word.strip() for word in line.split(' ')]
    train.append(line)
print(train)
"""构建词频矩阵，训练LDA模型"""
dictionary = corpora.Dictionary(train)
# corpus是把每条新闻ID化后的结果，每个元素是新闻中的每个词语，在字典中的ID和频率
corpus = [dictionary.doc2bow(text) for text in train]
print(corpus)
lda = models.LdaModel(corpus=corpus, id2word=dictionary, num_topics=20)
topic_list = lda.print_topics(20)
print("20个主题的单词分布为：\n")
for topic in topic_list:
    print(topic)
