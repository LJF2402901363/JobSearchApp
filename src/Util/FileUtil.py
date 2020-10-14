import re
import os


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
    def readDirFileToTex(textFileDirPath, ignoreWords):
        """
        将指定的文件夹的所有文本读取，然后使用正则表达式过滤掉不需要的词句
        :param textFileDirPath: 存放文本文件的文件夹路径
        :param ignoreWords: 要除去的词句的正则表达式
        :return:
        """
        # 返回一个列表，其中包含在目录条目的名称
        fileNameList = os.listdir(textFileDirPath)
        text = ''
        # 逐个读取文件夹中的文件到文本中
        for fileName in fileNameList:
            filePath = textFileDirPath + '/' + fileName
            if os.path.isfile(filePath):
                # 添加文件
                text = text + open(filePath, encoding='utf-8').read()
        # 替换除去要忽略的词
        txt = re.sub(ignoreWords, " ", text)
        return txt
