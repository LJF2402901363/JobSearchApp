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
        json_data = open(file=jsonFilePath, mode="r", encoding="utf8")
        jsonData = json.load(json_data)
        return jsonData

    @staticmethod
    def getFileAndImgProValueByKey(key):
        return JsonUtil.stc_fileAndImgPro[key]

    @staticmethod
    def getUrlSettingProValueByKey(key):
        return JsonUtil.stc_urlSettingPro[key]

    @staticmethod
    def jsonStrToJson(jsonStr):
        return json.loads(jsonStr)

    @staticmethod
    def jsonListToViewJson(jsonObj):
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
