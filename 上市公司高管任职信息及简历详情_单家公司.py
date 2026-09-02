import requests
import csv
from lxml import etree
from urllib.parse import urljoin


def manager_info(stockid):
    url=f"https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpManager/stockid/{stockid}.phtml"

    response=requests.get(url)
    text=response.text
    html=etree.HTML(text)
    row=html.xpath("//tr[td[1]//a[contains(@href,'vCI_CorpManagerInfo')] and normalize-space(td[2])!='']")

    pairs=[]
    for tr in row:
        name=''.join(tr.xpath('./td[1]//a//text()')).strip()
        position=''.join(tr.xpath('./td[2]//div//text()')).strip()
        start_tenure=''.join(tr.xpath('./td[3]//div//text()')).strip()
        final_tenure=''.join(tr.xpath('./td[4]//div//text()')).strip()

        href=''.join(tr.xpath('./td[1]//a//@href')).strip()
        url_de=urljoin(url,href)
        response_de=requests.get(url_de)
        text_de=response_de.text
        html_de=etree.HTML(text_de)
        resume=''.join(html_de.xpath("//td[contains(@class,'graybgH')]//text()")).strip()
        pairs.append((stockid,name,position,start_tenure,final_tenure,url_de,resume))
    return pairs

a=manager_info(600900)


with open(r'D:\高管任期.csv','w',newline='') as f:
    writer=csv.writer(f)
    writer.writerow(('股票代码','姓名','职务','开始日期','结束日期','链接','简历'))
    writer.writerows(a)


