from asyncio import as_completed
from concurrent.futures import ThreadPoolExecutor, as_completed
from Util.ThreadUtil import ThreadUtil
from Util.JobUtil import JobUtil
from Util.FileUtil import FileUtil
from Util.WordCloudUtil import WordCloudUtil
from Util.JsonUtil import JsonUtil
import json


class RequestService:
    def search(self, searchContent, proviceText, cityText):
        # 拼接要爬取数据的URL
        url = JsonUtil.getUrlSettingProValueByKey("searchUrl") + "?key=" + searchContent + "&dqs=&pageSize=80"
        # 获取爬取的所有JobInfo集合
        jobList = JobUtil.getJobList(url)
        wordText = ""
        for jobInfo in jobList:
            wordText = wordText + jobInfo.jobDes
        # 读取文本文件的路径
        textFilePath = JsonUtil.getFileAndImgProValueByKey('textFilePath')
        # 保存文本到指定的文件中去
        FileUtil.saveTextToFile(text=wordText, filePath=textFilePath)
        # 特殊符号和语句需要除去
        ignoreWords = JsonUtil.getFileAndImgProValueByKey('ignoreWords')
        # 读取文件中的字符串
        wordText = FileUtil.readFileToTex(textFilePath, ignoreWords)
        # 读取图片的路径
        smallImgPath = JsonUtil.getFileAndImgProValueByKey('wordCloudImg_small')
        # 读取背景图片的路径
        bgImgPath = JsonUtil.getFileAndImgProValueByKey('wordCloudBgImg')
        # 获取文本的词频率
        newWordsStr = JsonUtil.getFileAndImgProValueByKey('newWords')
        newWords = JsonUtil.jsonStrToJson(newWordsStr)
        # 从文本中获取分析后的json键值对
        jsonData = WordCloudUtil.getWordCouldJson(wordText, newWords)
        # 转化为json对象
        jsonObj = json.loads(jsonData)
        # 格式化返回json字符串
        jsonstr = JsonUtil.jsonListToViewJson(jsonObj, jobList)
        # 产生词云图片保存到指定的文件路径中
        WordCloudUtil.wordCould(wordText, bgImgPath, smallImgPath, 0.5)
        return jsonstr

    def handleSearchByThread(self, searchContent, proviceText, cityText):
        pageSize = JsonUtil.getUrlSettingProValueByKey("pageSize")
        searchUrl = JsonUtil.getUrlSettingProValueByKey("searchUrl")
        # 读取文本文件的路径
        textFilePathDir = JsonUtil.getFileAndImgProValueByKey('textFilePathDir')
        # 需要爬取的分页数，每个任务爬取一页
        pageCount = JsonUtil.getUrlSettingProValueByKey("pageCount")
        jobList = []
        # 使用多线程进行爬取数据
        with ThreadPoolExecutor(max_workers=pageCount) as t:
            obj_list = []
            for pageIndex in range(2):
                # 组装每页的职位URL
                url = searchUrl + "?key=" + searchContent + "&dqs=&pageSize=" + str(pageSize) + "&curPage=" + str(pageIndex)
                # 每个URL对应一个线程进行处理
                obj = t.submit(ThreadUtil.handleRequstByThread,url, textFilePathDir,searchContent + "-" + str(pageIndex))
                obj_list.append(obj)
            # pageJobInfoList
            for future in as_completed(obj_list):
                jsonFilePath = future.result()
                pageJobList = json.load(open(file=jsonFilePath,mode='r',encoding='utf8'))
                print("读取" + url + "完成。。。。")
                jobList.append(pageJobList)

        # 特殊符号和语句需要除去
        ignoreWords = JsonUtil.getFileAndImgProValueByKey('ignoreWords')
        # 读取文件中的字符串
        wordText = FileUtil.readDirFileToTex(textFilePathDir, ignoreWords)
        # 读取图片的路径
        smallImgPath = JsonUtil.getFileAndImgProValueByKey('wordCloudImg_small')
        # 读取背景图片的路径
        bgImgPath = JsonUtil.getFileAndImgProValueByKey('wordCloudBgImg')
        # 获取文本的词频率
        newWordsStr = JsonUtil.getFileAndImgProValueByKey('newWords')
        newWords = JsonUtil.jsonStrToJson(newWordsStr)
        # 从文本中获取分析后的json键值对
        jsonData = WordCloudUtil.getWordCouldJson(wordText, newWords)
        # 转化为json对象
        jsonObj = json.loads(jsonData)
        # 格式化返回json字符串
        jsonstr = JsonUtil.jsonListToViewJson(jsonObj, jobList)
        # 产生词云图片保存到指定的文件路径中
        WordCloudUtil.wordCould(wordText, bgImgPath, smallImgPath, 0.5)
        return jsonstr
