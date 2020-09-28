import re


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
    def readFileToTex(filename, ignoreWords):
        # 特殊符号和部分无意义的词
        txt = open(filename, encoding='utf-8').read()
        # 替换
        txt = re.sub(ignoreWords, " ", txt)
        return txt
