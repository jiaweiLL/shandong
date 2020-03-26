import xlrd
import jieba.analyse
from gensim import corpora, models, similarities

data = xlrd.open_workbook('news.xlsx', encoding_override='utf-8')
wordsdata=[]
txtName = "Word.txt"
f=open(txtName, "a+")

table = data.sheets()[0]
nrows = table.nrows
for i in range(1, nrows):
    alldata = table.row_values(i)
    result = alldata[0]
    # jieba.load_userdict('dict.txt')
    b = jieba.analyse.extract_tags(result, topK=20, withWeight=False, allowPOS=())
    l = len(b)
    for j in range(1,l):
        f.write(b[j]+" ")
fr = open('Word.txt', 'r', encoding='gbk')
train = []
for line in fr.readlines():
    line = [word.strip() for word in line.split(' ')]
    train.append(line)
print(train)
"""构建词频矩阵，训练LDA模型"""
dictionary = corpora.Dictionary(train)
# corpus是把每条新闻ID化后的结果，每个元素是新闻中的每个词语，在字典中的ID和频率
corpus = [dictionary.doc2bow(text) for text in train]

lda = models.LdaModel(corpus=corpus, id2word=dictionary, num_topics=20)
topic_list = lda.print_topics(20)
# print(topic_list)
print("20个主题的单词分布为：\n")
for topic in topic_list:
    print(topic)




