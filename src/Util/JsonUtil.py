import json


class JsonUtil:
    stc_fileAndImgPro = json.load(open(file="static/json/fileAndImgPro.json", mode="r", encoding="utf8"))
    stc_urlSettingPro = json.load(open("static/json/urlSettingPro.json", mode="r", encoding="utf8"))

    @staticmethod
    def transferObjectToJson(job):
        """
        将job对象的属性一一与json格式对应
        :param job:
        :return:
        """
        return {
            "jobSalary": job.jobSalary,
            "jobCity": job.jobCity,
            "jobEdu": job.jobEdu,
            "jobExperienceTime": job.jobExperienceTime,
            "jobDes": job.jobDes,
            "jobRequire": job.jobRequire,
            "codeName": job.codeName,
            "age": job.age
        }

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
    def jsonStrToJson(jsonStr):
        """
        将json字符串转化为json对象
        :param jsonStr:
        :return:
        """
        return json.loads(jsonStr)

    @staticmethod
    def jsonListToViewJson(jsonObj):
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
            "totalValue": value,
            "total":value
            }
        "status":1}
        :param jsonObj: 需要转换的json对象数组
        :return:
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
        jsonstr = jsonstr + '{"name":"其它","value":' + str(4)
        jsonstr = jsonstr + '}]},"status":1}'
        return jsonstr
