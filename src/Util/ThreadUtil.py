import threading
from Util.JobUtil import JobUtil
import json
from Util.FileUtil import FileUtil
from Util.JsonUtil import JsonUtil
import os

class ThreadUtil:
    @staticmethod
    def handleRequstByThread(jobUrl, saveFileDirPath, fileName):
        """
        开始处理jobURL对应的数据并存储到saveFilePath中
        :return:
        """
        # 获取URL中对应的所有工作的具体信息
        jobList = JobUtil.getJobList(jobUrl)
        # 将list数组转换为json格式的数组
        jobListJsonStr = JsonUtil.listToJson(jobList)

        # 保存文本到指定的文件中去
        if os.path.isdir(saveFileDirPath):
            filePath = saveFileDirPath + '/' + fileName + '.json'
            FileUtil.saveTextToFile(text=jobListJsonStr,filePath=filePath)
            print("保存文件"+fileName+"成功。。。。\n")
            return filePath
        return ''
