import pymysql
import xlrd
import jieba.analyse

if __name__ == '__main__':

    #TitleDic建立#######################################################/
    print("TitleDic正在建立...")
    data = xlrd.open_workbook('news.xlsx', encoding_override='utf-8')
    table = data.sheets()[0]
    nrows = table.nrows
    i = 1
    #创建表TitleDIc
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='tieba')
    curs = conn.cursor()#游标
    curs.execute("drop table if exists TitleDic")#写入
    curs.execute("create table TitleDic(id BIGINT)")
    conn.commit()
    curs.close()
    conn.close()
    for d in range(20):
        sql = "insert into TitleDic (id) VALUES(%s)" % d
        cxn = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='tieba')
        cur = cxn.cursor()
        # cur.execute(sqlc)
        cur.execute(sql)
        cxn.commit()
        cxn.close()
    for i in range(1, nrows):  # 第0行为表头
        alldata = table.row_values(i)  # 循环输出excel表中每一行，即所有数据
        # print(alldata)
        result = alldata[0]  # 取出表中第二列数据
        jieba.load_userdict('dict.txt')
        b = jieba.analyse.extract_tags(result, topK=20, withWeight=False, allowPOS=())
        l=len(b)
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root',db='tieba')
        curs = conn.cursor()
        #创建key%s列
        sqla = "alter table TitleDic add key%s text" % i
        curs.execute(sqla)
        conn.commit()
        curs.close()
        conn.close()
        #将帖子title的分词写入数据库
        for j in range(l):
            sql = "UPDATE TitleDic SET key%s='%s' WHERE id=%s;" % (i, b[j],j)
            cxn = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='tieba')
            cur = cxn.cursor()
            # cur.execute(sqlc)
            cur.execute(sql)
            cxn.commit()
            cur.close()
            cxn.close()
    print("TitleDic建立成功!")
    ###########################################################/



    #创建CommentsDic########################################
    print("CommentsDic正在建立...")
    data = xlrd.open_workbook('comments.xlsx', encoding_override='utf-8')
    table = data.sheets()[0]
    nrows = table.nrows
    ncols=table.ncols
    # print(ncols)
    i = 1
    # 创建表TitleDIc
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='tieba')
    curs = conn.cursor()
    curs.execute("drop table if exists CommentsDic")
    curs.execute("create table CommentsDic(id BIGINT)")
    conn.commit()
    curs.close()
    conn.close()
    for d in range(100):
        sql = "insert into CommentsDic (id) VALUES(%s)" % d
        cxn = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='tieba')
        cur = cxn.cursor()
        # cur.execute(sqlc)
        cur.execute(sql)
        cxn.commit()
        cxn.close()
    for i in range(1, ncols):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='tieba')
        curs = conn.cursor()
        # 创建key%s列
        sqla = "alter table CommentsDic add key%s text" % i
        curs.execute(sqla)
        conn.commit()
        curs.close()
        conn.close()
        sum=0

        for j in range(1,nrows):
            result = table.row_values(j)[i]  # 第j行第i列的值取出赋给result
            jieba.load_userdict('dict.txt')
            b = jieba.analyse.extract_tags(result, topK=20, withWeight=False, allowPOS=())
            l = len(b)
            if b!=[]:
                # 将帖子title的分词写入数据库
                for m in range(l):
                    sql = "UPDATE CommentsDic SET key%s='%s' WHERE id=%s;" % (i, b[m], sum)
                    cxn = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='tieba')
                    cur = cxn.cursor()
                    # cur.execute(sqlc)
                    cur.execute(sql)
                    cxn.commit()
                    cur.close()
                    cxn.close()
                    sum=sum+1
    print("CommentsDic建立成功!")
    ###########################################################/






















    #
    # for i in range(1, nrows):
    #     sql = "select * from TitleDic order by key%s desc" % i
    #     # sqlc = "ALTER TABLE TitleDic ALTER key%s SET DEFAULT 1000" % i
    #     # ret = dic2sql(b, sql)
    #     # print(ret)
    #     # 连接MySQL，并提交数据
    #     cxn = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='tieba')
    #     cur = cxn.cursor()
    #     # cur.execute(sqlc)
    #     cur.execute(sql)
    #     cxn.commit()
    #     cxn.close()
    # dic = {i: []}
        # for j in b:
        #     dic[i].append(j)
        # print(dic)
        # b(文本，为返回几个 TF/IDF 权重最大的关键词，默认值为 20，
        # 为是否一并返回关键词权重值，默认值为 False，仅包括指定词性的词，默认值为空，即不筛选)
        # c基于 TextRank 算法的关键词抽取
        # 1.将待抽取关键词的文本进行分词
        # 2.以固定窗口大小(默认为5，通过span属性调整)，词之间的共现关系，构建图
        # 3.计算图中节点的PageRank，注意是无向带权图
        # c = jieba.analyse.textrank(str, topK=20, withWeight=True, allowPOS=('n', 'nr', 'ns'))
        # jieba.lcut_for_search(result, HMM=True)
        # jieba.lcut(result)

#dic加入数据库
    # sql = "insert into users (login,userid) VALUES %s;"
    #
    # ret = dic2sql(dic, sql)
    # # print(ret)
    #
    # # 连接MySQL，并提交数据
    # cxn = pymysql.connect(user='root',password='root', db='tieba')
    # cur = cxn.cursor()
    # cur.execute(ret)
    # cxn.commit()
    # cxn.close()
# sql = "select * from TitleDic order by key%s desc" %3
#         # ret = dic2sql(b, sql)
#         # print(ret)
#         # 连接MySQL，并提交数据
# cxn = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='tieba')
# cur = cxn.cursor()
# cur.execute(sql)
# cxn.commit()
# cxn.close()



