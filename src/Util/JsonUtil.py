import json

from domain.JobInfo import JobInfo


class JsonUtil:
    # 加载fileAndImgPro.json配置文件
    stc_fileAndImgPro = json.load(open(file="static/json/fileAndImgPro.json", mode="r", encoding="utf8"))
    # 加载urlSettingPro.json配置文件
    stc_urlSettingPro = json.load(open(file="static/json/urlSettingPro.json", mode="r", encoding="utf8"))
    # 加载cityMapingJson.json配置文件
    stc_cityMapingPro = json.load(open(file="static/json/cityMapingJson.json", mode="r", encoding="utf8"))
    @staticmethod
    def readFileToJson(jsonFilePath):
        """
        将json文件读取为json对象
        :param jsonFilePath:
        :return:
        """
        json_data = open(file=jsonFilePath, mode="r", encoding="utf8")
        jsonData = json.load(json_data)
        return jsonData

    @staticmethod
    def getFileAndImgProValueByKey(key):
        """
        通过key来获取json对应的value值
        :param key: json对象中的key
        :return:
        """
        return JsonUtil.stc_fileAndImgPro[key]

    @staticmethod
    def getUrlSettingProValueByKey(key):
        """
        通过key来获取json对应的value值
        :param key: json对象中的key
        :return:
        """
        return JsonUtil.stc_urlSettingPro[key]

    @staticmethod
    def getCityMapingProValueByKey(cityMapJson,keyName):
        """
        通过key来获取json对应的value值
        :param key: json对象中的key
        :return:
        """
        for jsonCity in cityMapJson:
            if jsonCity['name'] == keyName:
                return jsonCity['value']
        return ''
    @staticmethod
    def jsonStrToJson(jsonStr):
        """
        将json字符串转化为json对象
        :param jsonStr:
        :return:
        """
        return json.loads(jsonStr)

    @staticmethod
    def jsonListToViewJson(jsonObj, jobList,wordCouldImgPath,status,msg):
        """
        将一个json对象转换为符合前端页面展示数据的json字符串
        格式：
        {
            "data":
            {
            "words":
            [
              { name: key}
            ],

            "jobInfoData":[{
            name:key
            }]
            },
            "wordCouldImg":"词云图保存路径",
            "status":1,
            "msg":"提示的内容"

        }
        "status":1}
        :param jobList: 所有职位的列表
        :param jsonObj: 需要转换的json对象数组
        :param wordCouldImgPath: 词云图的图片路径
        :param status: 状态
        :param msg: 返回前端页面的提示信息
        :return: 返回一个json格式字符串
        """
        jsonstr = '{ "data":{ "words":['
        index = 0
        count = 0
        for obj in jsonObj:
            index = index + 1
            if index <= 10:
                jsonstr = jsonstr + '{"name":"' + obj + '","value":' + str(jsonObj[obj]) + "},"
            else:
                count = count + jsonObj[obj]
        jsonstr = jsonstr + '{"name":"其它","value":' + str(4) + "}],"
        jobListStr = '"jobList":['
        size = len(jobList)
        for index in range(size):
            job = jobList[index]
            jobListStr = jobListStr + '{"name":"' + job.jobName + '",'
            jobListStr = jobListStr + '"city":"' + job.jobCity + '",'
            jobListStr = jobListStr + '"edu":"' + job.jobEdu + '",'
            jobListStr = jobListStr + '"salary":"' + str(job.jobSalary) + '",'
            jobListStr = jobListStr + '"experienceTime":"' + job.jobExperienceTime + '",'
            jobListStr = jobListStr + '"jobUrl":"' + job.jobUrl + '",'
            jobListStr = jobListStr + '"age":"' + job.age + '",'
            if index == size - 1:
                jobListStr = jobListStr + '"codeName":"' + job.codeName + '"}'
            else:
                jobListStr = jobListStr + '"codeName":"' + job.codeName + '"},'
        jsonstr = jsonstr + jobListStr + ']'
        jsonstr = jsonstr + ',"wordCouldImg":"' + wordCouldImgPath + '"}'
        jsonstr = jsonstr + ',"status":' + str(status) + ',"msg":"' + msg + '"}'
        # print(jsonstr)
        return jsonstr

    @staticmethod
    def listToJson(jobList):
        """
        将一个list转为json格式
        :param jobList:工作集合
        :return:返回工作信息的json格式字符串
        """
        size = len(jobList)
        jobListStr = '['
        for index in range(size):
            job = jobList[index]
            jobListStr = jobListStr + '{"name":"' + job.jobName + '",'
            jobListStr = jobListStr + '"city":"' + job.jobCity + '",'
            jobListStr = jobListStr + '"edu":"' + job.jobEdu + '",'
            jobListStr = jobListStr + '"salary":"' + str(job.jobSalary) + '",'
            jobListStr = jobListStr + '"experienceTime":"' + job.jobExperienceTime + '",'
            jobListStr = jobListStr + '"age":"' + job.age + '",'
            jobListStr = jobListStr + '"jobUrl":"' + job.jobUrl + '",'
            if index == size - 1:
                jobListStr = jobListStr + '"codeName":"' + job.codeName + '"}'
            else:
                jobListStr = jobListStr + '"codeName":"' + job.codeName + '"},'
        jobListStr = jobListStr + ']'
        return jobListStr

    @staticmethod
    def getJobListDesStr(jobList):
        """
        获取jobList中岗位要求的全部字符串
        :param jobList: 包含岗位集合的list
        :return:
        """
        jobListDesStr = ''
        for job in jobList:
            jobListDesStr = jobListDesStr + job.jobDes
        return jobListDesStr
    @staticmethod
    def readJsonFileToList(filePath):
        # 获取json格式的job信息集合
        jobJsonArray = json.load(open(file=filePath, encoding='utf-8'))
        # 用户保存工作对象的集合
        jobList = []
        for jobJson in jobJsonArray:
            # {"name":"Java后端高级开发工程师","city":"成都","edu":"本科及以上","salary":"12-18k·13薪",
            # "experienceTime":"3-5年","age":"年龄不限","codeName":"语言不限"}
            jobName = jobJson['name']
            jobCity = jobJson['city']
            jobEdu = jobJson['edu']
            jobSalary = jobJson['salary']
            jobExperienceTime = jobJson['experienceTime']
            jobAge = jobJson['age']
            jobCodeName = jobJson['codeName']
            jobUrl = jobJson['jobUrl']
            job = JobInfo()
            job.set_age(jobAge)
            job.set_jobEdu(jobEdu)
            job.set_jobCity(jobCity)
            job.set_jobExperienceTime(jobExperienceTime)
            job.set_codeName(jobCodeName)
            job.set_jobSalary(jobSalary)
            job.set_jobName(jobName)
            job.set_jobUrl(jobUrl)
            jobList.append(job)
        return  jobList
