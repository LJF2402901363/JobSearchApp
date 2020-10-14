from Util.JobUtil import JobUtil
from Util.FileUtil import FileUtil
from Util.JsonUtil import JsonUtil
import os

class ThreadUtil:
    @staticmethod
    def handleRequstByThread(jobUrl, saveFileDirPath, fileName):
        """
        开始处理jobURL对应的数据并存储到saveFileDirPath中
        :param jobUrl: 每页数据总URL，响应数据包含40个job的信息
        :param saveFileDirPath: 保存的信息到的目录（使用多线程每个线程负责一页数据，然后保存到一个文件）
        :param fileName: 文件名
        :return: 返回工作集合
        """
        # 获取URL中对应的所有工作的具体信息
        print("开始获取"+jobUrl+"的工作信息列表\n")
        jobList = JobUtil.getJobList(jobUrl)
        print("完成获取" + jobUrl + "的工作信息列表\n")
        # 将list数组转换为json格式的数组
        jobListJsonStr = JsonUtil.listToJson(jobList)
        jobDesStr = JsonUtil.getJobListDesStr(jobList)
        # print(jobListJsonStr)
        # 保存文本到指定的文件中去
        if os.path.isdir(saveFileDirPath):
            # 将工作具体的信息数据以json格式保存到指定文件的文件名
            jsonFilePath = saveFileDirPath + '/' + fileName + '.json'
            # 将工作岗位要求和描述以txt格式保存到指定文件的文件名
            desFilePath = saveFileDirPath + '/' + fileName + '.txt'
            # 将工作信息保到json文件中
            FileUtil.saveTextToFile(text=jobListJsonStr,filePath=jsonFilePath)
            # 将工作描述要求保存到txt文件中去
            FileUtil.saveTextToFile(text=jobDesStr, filePath=desFilePath)
            print("保存文件"+fileName+"成功。。。。\n")
        return jobList
