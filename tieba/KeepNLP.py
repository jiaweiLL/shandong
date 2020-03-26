import pymysql
import xlrd

if __name__ == '__main__':
    #NLP建立#######################################################/
    print("NLP正在建立...")
    data = xlrd.open_workbook('NLP.xlsx', encoding_override='utf-8')
    table = data.sheets()[0]
    nrows = table.nrows
    i = 1
    #创建表NLP
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='tieba')
    curs = conn.cursor()#游标
    curs.execute("drop table if exists NLP")
    curs.execute("create table NLP(id BIGINT )")
    sqla = "alter table NLP add nlp float"
    curs.execute(sqla)
    conn.commit()
    curs.close()
    conn.close()
    for d in range(nrows):
        sql = "insert into NLP (id) VALUES(%s)" % d
        cxn = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='tieba')
        cur = cxn.cursor()
        # cur.execute(sqlc)
        cur.execute(sql)
        cxn.commit()
        cxn.close()
    for i in range(nrows):
        alldata = table.row_values(i)
        data=[]
        for k in alldata:
            k=float(k)
            data.append(k)
        sql = "UPDATE NLP SET nlp=%f WHERE id=%s" % (data[0], i)
        cxn = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='tieba')
        cur = cxn.cursor()
        # cur.execute(sqlc)
        cur.execute(sql)
        cxn.commit()
        cur.close()
        cxn.close()
    print("NLP建立成功！")