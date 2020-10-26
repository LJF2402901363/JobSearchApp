from asyncio import as_completed
from concurrent.futures import ThreadPoolExecutor, as_completed
from Util.ThreadUtil import ThreadUtil
from Util.JobUtil import JobUtil
from Util.FileUtil import FileUtil
from Util.WordCloudUtil import WordCloudUtil
from Util.JsonUtil import JsonUtil
import json
import re
import os

class RequestService:
    def singleThreadHandleSearch(self, searchContent, proviceText, cityText):
        """
        单线程爬取请求
        :param searchContent:搜索的关键词
        :param proviceText: 省份
        :param cityText:市区
        :return:
        """
        try:
            # 用于所有工作对象存储的集合
            jobList = []
            # 所有工作的岗位要求和描述
            jobDesText = ''
            for jobProKey in JsonUtil.stc_urlSettingPro:
                jobPro = JsonUtil.stc_urlSettingPro[jobProKey]
                dqs = ''
                if len(str(proviceText)) == 0 and len(str(cityText)) == 0:
                    dqs = ''
                else:
                    # 获取urlSettingPro中城市对应maper的key
                    cityMaperName= jobPro['cityMaperName']
                    # 获取城市对应的编码json表
                    cityMapJson = JsonUtil.stc_cityMapingPro[cityMaperName]
                    cityCode = JsonUtil.getCityMapingProValueByKey(cityMapJson,cityText)
                    proviceCode = JsonUtil.getCityMapingProValueByKey(cityMapJson,proviceText)
                    if len(str(cityCode)) == 0 and len(str(proviceCode)) == 0:
                        return '{"status":0,"msg":"暂不支持搜索该城市哦"}'
                    else:
                        if len(str(cityCode)) != 0:
                            dqs = cityCode
                        else:
                            dqs = proviceCode
                # 每页的数量
                pageSize = JsonUtil.getUrlSettingProValueByKey("pageSize")
                # 需要爬取的分页数，每个任务爬取一页
                pageCount = JsonUtil.getUrlSettingProValueByKey("pageCount")
                # 具体爬取工作时的链接
                searchUrl = JsonUtil.getUrlSettingProValueByKey("searchUrl")
                # 特殊符号和语句需要除去
                ignoreWords = JsonUtil.getFileAndImgProValueByKey('ignoreWords')
                # 读取文本文件的所在文件夹
                textFileDirPath = JsonUtil.getFileAndImgProValueByKey('textFilePathDir')
                # 查看本地是有已经存储有该搜索条件匹配的，如果存在则直接从本地中获取，否则在网络上中获取.
                textDesFilePath = textFileDirPath + "/" + searchContent + "_" + dqs + ".txt"

                # 判断对应的文件名是否存在，如果存在则说明本地已经有该文件，否则没有
                if os.path.isfile(textDesFilePath):
                    # 或名该搜索已经缓存到本地,开始读取
                    jobDesText = FileUtil.readFileToTex(textDesFilePath, ignoreWords)
                    # 拼接所有工作信息json格式的文件名
                    jobJsonFilePath = textFileDirPath + "/" + searchContent + "_" + dqs + ".json"
                    # 读取json对应文件中的job数组
                    jobList = JsonUtil.readJsonFileToList(jobJsonFilePath)
                else:
                    for jobPro in JsonUtil.stc_urlSettingPro:
                        for i in range(pageCount):
                            print("开始爬取第" + str(i + 1) + "页数据\n")
                            print(searchUrl)
                            # 组装每页的职位URL
                            url = str(searchUrl).format(searchContent, dqs, pageSize, i)
                            # url = searchUrl + "?key=" + searchContent + "&dqs=" + dqs + "&pageSize=" + str(
                            #                     #     pageSize) + "&curPage=" + str(i)
                            # 获取爬取的所有JobInfo集合
                            pageJobList = JobUtil.getJobList(url, JsonUtil.stc_urlSettingPro[jobPro])
                            # 将获取的职位集合都保存到jobList
                            for job in pageJobList:
                                jobList.append(job)
                            print("爬取第" + str(i + 1) + "页数据完成。。\n")

                    # 所有工作岗位描述的文本内容
                    jobDesText = JsonUtil.getJobListDesStr(jobList)
                    # 拼接文件格名以txt格式保存,全部职位信息的要求都保存到同一个文件中去
                    textFilePath = textFileDirPath + "/" + searchContent + "_" + dqs + ".txt"
                    # 保存文本到指定的文件中去
                    FileUtil.saveTextToFile(text=jobDesText, filePath=textFilePath)
                    # 将jobList集合转换为json格式
                    jobListJsonStr = JsonUtil.listToJson(jobList)
                    # 拼接json格式的文件名
                    jsonFilePath = textFileDirPath + "/" + searchContent + "_" + dqs + ".json"
                    # 将所有的工作信息以json格式保存到文件中去
                    FileUtil.saveTextToFile(jobListJsonStr, jsonFilePath)

                # 读取图片的路径
                smallImgPath = JsonUtil.getFileAndImgProValueByKey('wordCloudImg')
                # 读取背景图片的路径
                bgImgPath = JsonUtil.getFileAndImgProValueByKey('wordCloudBgImg')
                # 获取文本的词频率
                newWordsStr = JsonUtil.getFileAndImgProValueByKey('newWords')
                # 将json格式的newWords字符串转换为json对象
                newWords = JsonUtil.jsonStrToJson(newWordsStr)
                # 从文本中获取分析后的json键值对
                jsonData = WordCloudUtil.getWordCouldJson(jobDesText, newWords)
                # 转化为json对象
                jsonObj = json.loads(jsonData)
                # 格式化返回json字符串
                status = 1
                msg = "搜索完成"
                jsonstr = JsonUtil.jsonListToViewJson(jsonObj, jobList, smallImgPath, status, msg)
                # 产生词云图片保存到指定的文件路径中
                WordCloudUtil.wordCould(jobDesText, bgImgPath, smallImgPath, 0.5)
                return jsonstr

        except:
            jsonstr = '{"status":0,"msg":"服务器发生错误！"}'
            return jsonstr

    def multiThreadHandleSearch(self, searchContent, proviceText, cityText):
        """
           多线程程爬取请求
           :param searchContent:搜索的关键词
           :param proviceText: 省份
           :param cityText:市区
           :return:
        """
        dqs = ''
        if len(str(proviceText)) == 0 and len(str(cityText)) == 0:
            dqs = ''
        else:
            cityCode = JsonUtil.getCityMapingProValueByKey(cityText)
            proviceCode = JsonUtil.getCityMapingProValueByKey(proviceText)
            if len(str(cityCode)) == 0 and len(str(proviceCode)) == 0:
                return '{"status":0,"msg":"暂不支持搜索该城市哦"}'
            else:
                if len(str(cityCode)) != 0:
                    dqs = cityCode
                else:
                    dqs = proviceCode
        # 每页的数据
        pageSize = JsonUtil.getUrlSettingProValueByKey("pageSize")
        # 爬取职位时的具体路径
        searchUrl = JsonUtil.getUrlSettingProValueByKey("searchUrl")
        # 读取文本文件的路径
        textFilePathDir = JsonUtil.getFileAndImgProValueByKey('textFilePathDir')
        # 特殊符号和语句需要除去
        ignoreWords = JsonUtil.getFileAndImgProValueByKey('ignoreWords')
        # 需要爬取的分页数，每个任务爬取一页
        pageCount = JsonUtil.getUrlSettingProValueByKey("pageCount")
        # 拼接每个文件的文件前缀名，比如  搜索关键词为： 算法 ，搜索的区域对应的编号码为 010,并且是第1页数据，那么json文件名为： 算法_010_0.json，岗位描述文本文件名：算法_010_0.txt
        preFileName = searchContent + "_" + dqs + "_"
        wordText = FileUtil.readDesFileInDirToTex(textFilePathDir, preFileName, ignoreWords)
        pageJobInfoList = []
        if len(wordText) != 0:
            pageJobInfoList = FileUtil.readJsonFileInDirToTex(textFilePathDir, preFileName, ignoreWords)
        else:
            # 使用多线程进行爬取数据
            with ThreadPoolExecutor(max_workers=pageCount) as t:
                obj_list = []
                for pageIndex in range(pageCount):
                    # 组装每页的职位URL
                    url = searchUrl + "?key=" + searchContent + "&dqs=" + dqs + "&pageSize=" + str(
                        pageSize) + "&curPage=" + str(pageIndex)
                    # 每个URL对应一个线程进行处理
                    # 拼接每个文件名： 搜索内容_城市编码_索引编号
                    fileName = searchContent + "_" + dqs + "_" + str(pageIndex)
                    obj = t.submit(ThreadUtil.handleRequstByThread, url, textFilePathDir, fileName)
                    print("开始" + url + "线程。。。。\n")
                    obj_list.append(obj)
                # pageJobInfoList
                print("。。。。等待多线程完成。。。。\n")
                for future in as_completed(obj_list):
                    jobList = future.result()
                    # 读取文件中的工作描述信息
                    wordText = JsonUtil.getJobListDesStr(jobList)
                    # 除去要忽略的词
                    wordText = re.sub(ignoreWords, " ", wordText)
                    print("读取" + url + "完成。。。。\n")
                    for job in jobList:
                        pageJobInfoList.append(job)
        # 读取图片的路径
        smallImgPath = JsonUtil.getFileAndImgProValueByKey('wordCloudImg_small')
        # 读取背景图片的路径
        bgImgPath = JsonUtil.getFileAndImgProValueByKey('wordCloudBgImg')
        # 获取文本的词频率
        newWordsStr = JsonUtil.getFileAndImgProValueByKey('newWords')
        # 将字符串转换为json对象
        newWords = JsonUtil.jsonStrToJson(newWordsStr)
        # 从文本中获取分析后的json键值对
        jsonData = WordCloudUtil.getWordCouldJson(wordText, newWords)
        # 转化为json对象
        jsonObj = json.loads(jsonData)
        # 格式化返回json字符串
        jsonstr = JsonUtil.jsonListToViewJson(jsonObj, pageJobInfoList)
        # 产生词云图片保存到指定的文件路径中
        WordCloudUtil.wordCould(wordText, bgImgPath, smallImgPath, 0.5)
        return jsonstr
