import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from domain.JobInfo import JobInfo
from Util.JsonUtil import JsonUtil


class JobUtil:
    stc_urlSettingPro = JsonUtil.stc_urlSettingPro

    @staticmethod
    def getHtmlTex(url):
        # 生成随机请求头
        header = {"User-Agent": UserAgent().random}
        # 获取请求内容
        response = requests.get(url=url, headers=header)
        # 判定是否成功获取
        if response.status_code != 200:
            raise Exception("请检查您的URL" + url)
        return response.text

    @staticmethod
    def getJobInfo(url):
        # 获取请求URL的对应返回HTML源代码
        html_tex = JobUtil.getHtmlTex(url)
        # 构建解析对象
        soup = BeautifulSoup(html_tex, "html.parser")
        # 获取所有包含职业名称以及职业详细链接的a标签
        jobInfo = JobInfo()
        # 获取工作的名称
        # jobNameDiv = soup.select("div.title-info > h1")
        jobNameDiv = soup.select(JsonUtil.getUrlSettingProValueByKey("jobNameDiv")['name1'])
        if len(jobNameDiv) > 0:
            jobName = jobNameDiv[0].text
            jobInfo.set_jobName(jobName)
        else:
            jobNameDiv = JobUtil.reGetJboName(url)
            if len(jobNameDiv) > 0:
                jobName = jobNameDiv[0].text
                jobInfo.set_jobName(jobName)
            else:
                print("jobName+" + url)
        # 获取公司名称信息
        jobCompanyDiv = soup.select(JsonUtil.getUrlSettingProValueByKey("jobCompanyNameDiv")['name1'])
        if len(jobCompanyDiv) > 0:
            jobCompany = jobCompanyDiv[0].text
            jobInfo.set_companyName(jobCompany)
        else:
            jobCompanyDiv = JobUtil.reGetJboCompany(url)
            if len(jobCompanyDiv) > 0:
                jobCompany = jobCompanyDiv[0].text
                jobInfo.set_companyName(jobCompany)
            else:
                print("jobCompany:" + url)
        #   获取薪水
        jobSalaryDivJson = JsonUtil.getUrlSettingProValueByKey("jobSalaryDiv")
        jobSalaryFla = False
        for key in jobSalaryDivJson:
            jobSalaryDiv = soup.select(jobSalaryDivJson[key])
            if len(jobSalaryDiv) > 0:
                jobSalary = jobSalaryDiv[0].text.rstrip()
                jobInfo.set_jobSalary(jobSalary)
                jobSalaryFla = True
                break
        # 获取不到需要重新发送请求获取
        if not jobSalaryFla:
            while 1 == 1:
                jobSalaryDiv = JobUtil.reGetJobSalary(url)
                if jobSalaryDiv is None:
                    continue
                if  len(list(jobSalaryDiv)) > 0:
                    jobSalary = jobSalaryDiv[0].text.rstrip()
                    jobInfo.set_jobSalary(jobSalary)
                    break
                else:
                    print("薪水：" + url)
        #    获取工作要求
        jobQualificationsDiv = soup.select(JsonUtil.getUrlSettingProValueByKey("jobQualificationsDiv")["name1"])
        while 1 == 1:
            if len(jobQualificationsDiv) > 0:
                index = 0
                for jobQualification in jobQualificationsDiv:
                    index = index + 1
                    text = jobQualification.text
                    # print(text)
                    if text is None or text == '':
                        print("url")
                    else:
                        if index == 1:
                            # 职位学历要求
                            jobInfo.set_jobEdu(text)
                        elif index == 2:
                            # 职位经验要求
                            jobInfo.set_jobExperienceTime(text)
                        elif index == 3:
                            # 职位编程语言要求
                            jobInfo.set_codeName(text)
                        elif index == 4:
                            # 求职者年龄要求
                            jobInfo.set_age(text)
                break
            else:
                # 重复获取
                jobQualificationsDiv = JobUtil.reGetJboAge(url)
        # 获取岗位描述
        jobDesDiv = JsonUtil.getUrlSettingProValueByKey("jobDesDiv")
        jobDesDivFla = False
        for key in jobDesDiv:
            jobDes = soup.select(jobDesDiv[key])
            if len(jobDes) > 0:
                jobInfo.set_jobDes(jobDes[0].text)
                jobDesDivFla = True
                break
        # 获取不到重新发送请求获取
        if not jobSalaryFla:
            while 1 == 1:
                jobDes = JobUtil.reGetJboDes(url)
                if len(jobDes) > 0:
                    jobInfo.set_jobDes(jobDes[0].text)
                    break
                else:
                    print("jobDes:" + url)
        return jobInfo


    @staticmethod
    def reGetJboName(url):
        """
        重新发送请求获取工作名称的标签块
        :param url: 该工作的具体信息URL
        :return: 返回工作名称的标签块
        """
        # 获取请求URL的对应返回HTML源代码
        html_tex = JobUtil.getHtmlTex(url)
        # 构建解析对象
        soup = BeautifulSoup(html_tex, "html.parser")
        # 获取工作名称
        jobNameDiv = soup.select(JsonUtil.getUrlSettingProValueByKey("jobNameDiv")['name1'])
        return jobNameDiv

    @staticmethod
    def reGetJboAge(url):
        """
        重新发送请求然后获取求职者年龄标签块
        :param url: 该工作的具体信息URL
        :return: 返回求职者年龄标签块
        """
        # 获取请求URL的对应返回HTML源代码
        html_tex = JobUtil.getHtmlTex(url)
        # 构建解析对象
        soup = BeautifulSoup(html_tex, "html.parser")
        # 获取年龄标签块
        JboAgeDiv = soup.select(JsonUtil.getUrlSettingProValueByKey("jobAgeDiv")['name1'])
        return JboAgeDiv

    @staticmethod
    def reGetJobSalary(url):
        """
        重新发送请求获取工作薪水的标签
        :param url: 该工作具体信息的URL
        :return: 返回一个薪水标签块
        """
        # 获取请求URL的对应返回HTML源代码
        html_tex = JobUtil.getHtmlTex(url)
        # 构建解析对象
        soup = BeautifulSoup(html_tex, "html.parser")
        jobSalaryDivJson = JsonUtil.getUrlSettingProValueByKey("jobSalaryDiv")
        for key in jobSalaryDivJson:
            # 获取薪资标签块
            jobSalaryDiv = soup.select(jobSalaryDivJson[key])
            if len(list(jobSalaryDiv)) > 0:
                return jobSalaryDiv
            else:
                print("jobSarlary为空！")



    @staticmethod
    def reGetJboCompany(url):
        """
        重新发送请求获取工作公司的标签块
        :param url: 该工作信息的URL
        :return: 返回工作公司的标签块
        """
        # 获取请求URL的对应返回HTML源代码
        html_tex = JobUtil.getHtmlTex(url)
        # 构建解析对象
        soup = BeautifulSoup(html_tex, "html.parser")
        # 获取所有包含职业名称以及职业详细链接的a标签
        jobCompanyDiv = soup.select("div.title-info h3")
        return jobCompanyDiv

    @staticmethod
    def reGetJboDes(url):
        """
        重新发送请求获取工作描述的标签快
        :param url: 指定的URL
        :return: 返回工作描述的标签块
        """
        # 获取请求URL的对应返回HTML源代码
        html_tex = JobUtil.getHtmlTex(url)
        # 构建解析对象
        soup = BeautifulSoup(html_tex, "html.parser")
        # 获取所有包含职业名称以及职业详细链接的a标签
        jobDesDiv = soup.select(JsonUtil.getUrlSettingProValueByKey("jobDesDiv")['name1'])
        if len(jobDesDiv) == 0:
            jobDesDiv = soup.select(JsonUtil.getUrlSettingProValueByKey("jobDesDiv")['name2'])
        return jobDesDiv

    @staticmethod
    def getJobList(url):
        """
        获取URL对应的所有的职位信息集合
        :param url: 指定的URL
        :return: 返回职位对象的集合
        """
        # 获取请求URL的对应返回HTML源代码
        html_tex = JobUtil.getHtmlTex(url)
        jobList = []
        # 构建解析对象
        soup = BeautifulSoup(html_tex, "html.parser")
        # 获取所有包含职业名称以及职业详细链接的a标签
        jobInfoDiv = soup.select(JsonUtil.getUrlSettingProValueByKey("jobInfoLinkDiv")['name1'])
        for div in jobInfoDiv:
            # 将职位的详细链接添加到对应的集合中去
            jobInfoLink = div['href']
            if jobInfoLink.startswith("http"):
                jobInfo = JobUtil.getJobInfo(jobInfoLink)
                jobList.append(jobInfo)
            else:
                jobInfo = JobUtil.getJobInfo("https://www.liepin.com/" + jobInfoLink)
                jobList.append(jobInfo)
        return jobList
