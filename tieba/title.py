from urllib.request import urlopen
import xlwt
from snownlp import SnowNLP
from bs4 import BeautifulSoup

n1=int(input("请输入爬取帖子数量50*"))
n=n1*50
i = 0
p=0
j = 0
index=1
#新建工作簿,设置编码为utf-8
wb=xlwt.Workbook( encoding="utf-8" )
nlp=xlwt.Workbook( encoding="utf-8" )
baseurl=xlwt.Workbook( encoding="utf-8" )
#添加工作表,参数表示是否可以覆盖写入，True代表可以
sh = wb.add_sheet("sheet1", True)
nl=nlp.add_sheet("sheet1",True)
base=baseurl.add_sheet("sheet1",True)
# str2=(input())
# f = codecs.open("douban.xls", "wb", "utf-8")
# str1=str(input("请输入爬取的贴吧网址"))
print("正在爬取...")

while i < n:
    a = "https://tieba.baidu.com/f?kw=%CC%A9%B0%B2&fr=ala0&tpl=5&traceid="
    # a=(input("请输入爬取的贴吧网址"))
    i += 50
    z = (i / 50)
    print("第" + str(z) + "页")
    html = urlopen(a)
    # wb1 = openpyxl.load_workbook("news.xlsx")
    # wbs=wb["sheet1"]
    # wb.remove(wbs)
    # wb1.save("newx.xlxs")

    bsObj = BeautifulSoup(html, "html.parser")
    for links in bsObj.findAll("a", {"class": "j_th_tit"}):

        url='https://tieba.baidu.com/%s' % links.attrs["href"]
        # print(str(j) + " " + links.attrs["href"] + "  " +links.text)
        # print(links.text)
        # sh.write(j, 0, links.text)
        base.write(j, 0,url )
        s = SnowNLP(links.text)
        sh.write(j, 0, links.text)
        nl.write(j, 0, s.sentiments)
        baseurl.save('baseurl.xlsx')
        wb.save('news.xlsx')
        nlp.save('NLP.xlsx')
        j = j + 1
print("爬取成功！")
