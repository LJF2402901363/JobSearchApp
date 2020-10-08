import requests
from bs4 import BeautifulSoup
import re
from fake_useragent import UserAgent
import json

def getValue(text, pattern):
    for item in pattern:
        html = BeautifulSoup(text, "html.parser")
        jobName = html.select_one(item)
        if not jobName is None:
            return jobName.text
    return ""
def test():
    url = "https://www.liepin.com/zhaopin/?key=数据挖掘&dqs=010&pageSize=40&d_curPage=0&d_pageSize=40&d_headId" \
          "=349594eedb1eff68a382809e8213380b&curPage=2 "
    # 生成随机请求头
    header = {"User-Agent": UserAgent().random}
    response = requests.get(url, headers=header)
    html = BeautifulSoup(response.text, "html.parser")
    jobInfoDiv = html.select(".job-info")
    linkList = []
    JobNamelist = ["div.title-info > h1"]
    jobSalarylist = ["div.job-title-left > p.job-item-title"]
    jobCompanyNameList = ["div.title-info > h3 > a"]
    jobCityNameList = [" div.job-title-left > p.basic-infor > span > a"]
    jobEduList = ["div.job-title-left > div > span:nth-of-type(1)"]

    jobExperienceTimeList = ["div.job-title-left > div > span:nth-of-type(2)"]
    jobCodeNmaeList = ["div.job-title-left > div > span:nth-of-type(3)"]
    jobAgeList = ["div.job-title-left > div > span:nth-of-type(4)"]

    for jobInfo in jobInfoDiv:
        item = str(jobInfo)
        item_tex = re.findall(re.compile(r'<a.*href="(.*?)"'), item)[0]
        if not item_tex.startswith("http"):
            item_tex = "https://www.liepin.com/" + item_tex
        response = requests.get(item_tex, headers={"User-Agent": UserAgent().random})
        html_tex = response.text
        # mainDiv = html.select(".job-title-left")
        # if len(mainDiv) == 0:
        #     print("获取路径不对！"+item_tex)
        # print(mainDiv)
        # print(jobName)
        # print(salary)
        jobCompanyName = getValue(html_tex, jobCompanyNameList)
        print(jobCompanyName)
        # jobName = getValue(html_tex,JobNamelist)
        # salary = getValue(html_tex,jobSalarylist)
        # print(salary)
        # print(jobName)
        # print(jobMain)
        # city = getValue(html_tex, jobCityNameList)
        # print(city)
        # edu = getValue(html_tex, jobEduList)
        # print(edu)
        # jobExperienceTime = getValue(html_tex, jobExperienceTimeList)
        # print(jobExperienceTime)
        codeName = getValue(html_tex, jobCodeNmaeList)
        print(codeName)
        age = getValue(html_tex, jobAgeList)
        print(age)
        linkList.append(item_tex)

if __name__ == '__main__':

    # text = open(file="urlSettingPro.json", mode="r", encoding="utf8").read()
    jsonObj = json.load(open(file="urlSettingPro.json", mode="r", encoding="utf8"))

    # for obj  in jsonObj:
    #     print(obj,end='--->')
    #     value = jsonObj[obj]
    #     print(value)
    objJson = jsonObj['jobSalaryDiv']
    for obj in objJson:
        print(obj, end='--->')
        value = objJson[obj]
        print(value)