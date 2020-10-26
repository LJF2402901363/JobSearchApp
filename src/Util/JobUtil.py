import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from domain.JobInfo import JobInfo
from Util.JsonUtil import JsonUtil


class JobUtil:
    stc_urlSettingPro = JsonUtil.stc_urlSettingPro
    @staticmethod
    def getHtmlTex(url):
        """
        获取url对应的网页内容，即获取网页的源码便于分析
        :param url:
        :return:
        """
        # 生成随机请求头
        header = {"User-Agent": UserAgent().random}

        # 获取请求内容
        response = requests.get(url=url, headers=header)
        # 判定是否成功获取
        if response.status_code != 200:
            raise Exception("请检查您的URL" + url)
        return response.text


    @staticmethod
    def getJobList(url,jobPro):
        """
        获取URL对应的所有的职位信息集合
        :param url: 指定的URL
        :return: 返回职位对象的集合
        """
        # 获取请求URL的对应返回HTML源代码
        html_tex = JobUtil.getHtmlTex(url)
        # print(html_tex)
        jobList = []
        # 构建解析对象
        soup = BeautifulSoup(html_tex, "html.parser")
        # 获取所有包含职业名称以及职业详细链接的a标签
        jobInfoDiv = JobUtil.getValue(html_tex, jobPro["jobInfoLinkDiv"])
        for div in jobInfoDiv:
             try:
                # 将职位的详细链接添加到对应的集合中去
                jobInfoLink = div['href']
                if not jobInfoLink.startswith("http"):
                    # 有些job的URL是不完整的需要补充,比如：/a/21271755.shtml，则要补偿为： https://www.liepin.com/a/21271755.shtml
                    jobInfoLink = jobPro["url"] + jobInfoLink
                # 开始通过URL链接获取工作的具体封装信息
                jobInfo = JobUtil.getJobInfo(jobInfoLink,jobPro)
                # 剔除那些职位爬取不到完整数据的情况
                if not (len(jobInfo.jobName) == 0 or len(jobInfo.jobUrl) == 0):

                    jobList.append(jobInfo)
             except:
                print("读取jobURL" + url + "对应信息有误。。")

        return jobList
    @staticmethod
    def getJobInfo(jobInfoUrl,jobPro):
        """
        通过工作的详细信息URL获取对应的封装对象
        :param jobInfoUrl: 工作的详细信息URL
        :return: 返回一个JobInfo对象
        """
        # 实例化对象
        jobInfo = JobInfo()
        # 设置该工作的URL
        jobInfo.set_jobUrl(jobInfoUrl)
        # 获取工作URL详细的信息的网页源码
        html_tex = JobUtil.getHtmlTex(jobInfoUrl)
        # 获取工作名称
        jobName = JobUtil.getValue(html_tex, jobPro["jobNameDiv"])
        jobInfo.set_jobName(jobName.replace('"',''))
        # print(jobName)
        # 获取薪水
        salary = JobUtil.getValue(html_tex, jobPro["jobSalaryDiv"])
        jobInfo.set_jobSalary(salary.strip())
        # print(salary)
        # 获取公司名称
        jobCompanyName = JobUtil.getValue(html_tex, jobPro["jobCompanyNameDiv"])
        jobInfo.set_companyName(jobCompanyName.strip())
        # print(jobCompanyName)
        # 获取工作所在城市
        city = JobUtil.getValue(html_tex, jobPro["jobCityDiv"])
        jobInfo.set_jobCity(city.strip())
        # print(city)
        # 获取工作要求的文凭
        edu = JobUtil.getValue(html_tex, jobPro["jobEduDiv"])
        jobInfo.set_jobEdu(edu.strip())
        # print(edu)
        # 获取工作经验年长
        jobExperienceTime = JobUtil.getValue(html_tex, jobPro["jobExperienceTimeDiv"])
        # print(jobExperienceTime)
        jobInfo.set_jobExperienceTime(jobExperienceTime.strip())
        # 获取需要经过的编程语言
        codeName = JobUtil.getValue(html_tex, jobPro["jobCodeNameDiv"])
        # print(codeName)
        jobInfo.set_codeName(codeName.strip())
        # 获取工作要求的年龄限制
        age = JobUtil.getValue(html_tex, jobPro["jobAgeDiv"])
        jobInfo.set_age(age.strip())
        # print(age)
        # 获取工作的详细描述，职责要求
        jobDes = JobUtil.getValue(html_tex, jobPro["jobDesDiv"])
        jobDes = jobDes.replace(' ','').replace('\\','\\\\')
        jobInfo.set_jobDes(jobDes)
        # print(jobDes)


        return jobInfo
    @staticmethod
    def getValue(text, patternJson):
        """
        通过网页源码以及某个工作字段的选择器json数组来获取工作的属性
        :param text: 网页源码
        :param patternJson: 某个工作字段的选择器json数组，比如 薪水的字段对应的选择器有三个，那么其对应的json字符串为 {"name1":value1,"name2":value2,"name3":value3}
        :return: 返回某个字段的内容
        """
        for key in patternJson:
            html = BeautifulSoup(text, "html.parser")
            jobNameDiv = html.select_one(patternJson[key])
            if not jobNameDiv is None:
                return jobNameDiv.text
        return ""
