from sklearn.feature_extraction.text import  TfidfVectorizer
from sklearn.cluster import KMeans
import jieba
import xlrd
import jieba.analyse
from wordcloud import WordCloud, STOPWORDS
from imageio import imread
from sklearn.feature_extraction.text import CountVectorizer
import jieba
import csv
def jieba_tokenize(text):
    return jieba.lcut(text)
tfidf_vectorizer = TfidfVectorizer(tokenizer=jieba_tokenize, lowercase=False)
'''
tokenizer: 指定分词函数
lowercase: 在分词之前将所有的文本转换成小写，因为涉及到中文文本处理，
所以最好是False
'''
data = xlrd.open_workbook('news.xlsx','r', encoding_override='utf-8')
table = data.sheets()[0]
nrows = table.nrows
text_list=[]
for i in range(1, nrows):
    alldata = table.row_values(i)
    result = alldata[0]
    b = jieba.analyse.extract_tags(result, topK=20, withWeight=False, allowPOS=())
    l = len(b)
    for j in range(l):
        text_list.append(b[j])
        # print(b[j])
        # print(result)

print(text_list)
tfidf_matrix = tfidf_vectorizer.fit_transform(text_list)

num_clusters = 20
km_cluster = KMeans(n_clusters=num_clusters, max_iter=500, n_init=5, \
                    init='k-means++',n_jobs=1)
'''
n_clusters: 指定K的值
max_iter: 对于单次初始值计算的最大迭代次数
n_init: 重新选择初始值的次数
init: 制定初始值选择的算法
n_jobs: 进程个数，为-1的时候是指默认跑满CPU
注意，这个对于单个初始值的计算始终只会使用单进程计算，
并行计算只是针对与不同初始值的计算。比如n_init=10，n_jobs=40, 
服务器上面有20个CPU可以开40个进程，最终只会开10个进程
'''
#返回各自文本的所被分配到的类索引
result = km_cluster.fit_predict(tfidf_matrix)
# print(len(a))
index=0
word_list=[]
for i in result:
    if i!=0:
        word_list.append(text_list[index])
    index=index+1
print("Predicting result: ", result)
contents_list = " ".join(word_list)
print("contents_list变量的类型：", type(contents_list))

# 制作词云图，collocations避免词云图中词的重复，mask定义词云图的形状，图片要有背景色
wc = WordCloud(stopwords=STOPWORDS.add("一个"), collocations=False,
               background_color="white",
               font_path=r"C:\Windows\Fonts\simhei.ttf",
               width=400, height=300, random_state=42,
               mask=imread('back2.png',pilmode="RGB"))
wc.generate(contents_list)
wc.to_file("WordCould_title.png")

# 使用CountVectorizer统计词频
cv = CountVectorizer()
contents_count = cv.fit_transform([contents_list])
# 词有哪些
list1 = cv.get_feature_names()
# 词的频率
list2 = contents_count.toarray().tolist()[0]
# 将词与频率一一对应
contents_dict = dict(zip(list1, list2))
# 输出csv文件,newline=""，解决输出的csv隔行问题
with open("title_word.csv", 'w', newline="") as f:
    writer = csv.writer(f)
    for key, value in contents_dict.items():
        writer.writerow([key, value])
print("Predicting result: ", result)
# print(type(result))