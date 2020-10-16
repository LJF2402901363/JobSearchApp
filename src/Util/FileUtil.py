import re
import os
import json
from domain.JobInfo import JobInfo
from Util.JsonUtil import JsonUtil
class FileUtil:
    @staticmethod
    def saveTextToFile(text, filePath):
        """
        将文本内容text保存到filePath路径中去
        :param text: 要保存的文本
        :param filePath: 保存到的路径
        :return:
        """
        # 打开文件
        file = open(filePath, mode="tw", encoding="utf8")
        # 将文本写入文件中去
        file.write(text)
        # 刷新缓冲区
        file.flush()
        # 关闭文件资源
        file.close()

    @staticmethod
    def readFileToTex(textFilePath, ignoreWords):
        """
        将指定的文件内的文本读取，然后使用正则表达式过滤掉不需要的词句
        :param textFilePath: 文本文件路径
        :param ignoreWords: 要除去的词句的正则表达式
        :return:
        """

        # 特殊符号和部分无意义的词
        txt = open(textFilePath, encoding='utf-8').read()
        # 替换
        txt = re.sub(ignoreWords, " ", txt)
        return txt

    @staticmethod
    def readDesFileInDirToTex(textFileDirPath, desTxtFileName, ignoreWords):
        """
        将指定的文件夹的所有文本读取，然后使用正则表达式过滤掉不需要的词句
        :param desTxtFileName: 文件名
        :param textFileDirPath: 存放文本文件的文件夹路径
        :param ignoreWords: 要除去的词句的正则表达式
        :return:
        """
        # 返回一个列表，其中包含在目录条目的名称
        fileNameList = os.listdir(textFileDirPath)
        text = ''
        # 逐个读取文件夹中的文件到文本中
        for fileName in fileNameList:
            # 找到与jsonFileName对应的文件
            if fileName.startswith(desTxtFileName) and fileName.endswith('.txt'):
                # 拼接完整的文件路径
                filePath = textFileDirPath + '/' + fileName
                # 判断是否是文件
                if os.path.isfile(filePath):
                    # 添加文件
                    text = text + open(filePath, encoding='utf-8').read()

        # 替换除去要忽略的词
        txt = re.sub(ignoreWords, " ", text)
        return txt

    @staticmethod
    def readJsonFileInDirToTex(jsonFileDirPath, jsonFileName, ignoreWords):
        """
        将指定的文件夹的所有文本读取，然后使用正则表达式过滤掉不需要的词句
        :param jsonFileName: json文件名
        :param jsonFileDirPath: 存放文本文件的文件夹路径
        :param ignoreWords: 要除去的词句的正则表达式
        :return: 返回所有json文件中的job的实例对象集合
        """
        # 返回一个列表，其中包含在目录条目的名称
        fileNameList = os.listdir(jsonFileDirPath)
        text = ''
        jobList = []
        # 逐个读取文件夹中的文件到文本中
        for fileName in fileNameList:
            # 找到与jsonFileName对应的文件
            if fileName.startswith(jsonFileName) and fileName.endswith('.json'):
                print("读取json文件中的数据。。。。\n")
                # 拼接完整的文件路径
                filePath = jsonFileDirPath + '/' + fileName
                # 判断是否是文件
                if os.path.isfile(filePath):
                    # 获取该json文件下对应的Job数组
                    pageJobList = JsonUtil.readJsonFileToList(filePath)
                    # 将每个工作添加到jobList中
                    for job in pageJobList:
                        jobList.append(job)
        return jobList
