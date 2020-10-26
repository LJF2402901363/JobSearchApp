#e24.1AutoKeywordSearch.py
import requests
from bs4 import BeautifulSoup
import re
import json
def getKeywordResult(keyword):
    url ='http://www.baidu.com/s?wd='+keyword
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return ""
def parserLinks(html):
    soup = BeautifulSoup(html, "html.parser")
    links = []
    mylist=[]
    for div in soup.find_all('div', {'data-tools': re.compile('title')}):
        data = div.attrs['data-tools']  #获得属性值
        d = json.loads(data)        #将属性值转换成字典
        links.append(d['title']+'\n     '+d['url'])    #将返回链接的题目返回
     #   mylist.append(links)
   # return mylist
    return links
def main():
    html = getKeywordResult('Python')
    ls = parserLinks(html)
    count = 1
    for i in ls:
        print("[{:^3}]{}".format(count,i))
        count += 1
main()
