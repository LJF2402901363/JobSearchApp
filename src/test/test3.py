import requests
from bs4 import BeautifulSoup

allUniv = []


def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return ""


def fillUnivList(soup):
    data = soup.find_all('tr')
    for tr in data:
        ltd = tr.find_all('td')
        if len(ltd) == 0:
            continue
        singleUniv = []

        for td in ltd:
            singleUniv.append(td.text.strip())
        allUniv.append(singleUniv)


def printUnivList(num):
    print("{1:^2}{2:{0}^13}{3:{0}^3}{4:{0}^6}{5:{0}<6}{6:{0}<5}".format(chr(12288), "排名", "学校名称", "省市", "类型", "总分",
                                                                        "办学层次"))
    print("---------------------------------------------------------------------")
    for i in range(num):
        u = allUniv[i]
        print("{1:^2}{2:{0}^14}{3:{0}^3}{4:{0}^6}{5:{0}<10.1f}{6:{0}<5}".format(chr(12288), u[0], u[1], u[2], u[3],
                                                                                eval(u[4]), u[5]))
        print("---------------------------------------------------------------------")


def main(num):
    url = 'https://www.shanghairanking.cn/rankings/bcur/2020'
    html = getHTMLText(url)
    soup = BeautifulSoup(html, "html.parser")
    fillUnivList(soup)
    printUnivList(num)


main(10)
