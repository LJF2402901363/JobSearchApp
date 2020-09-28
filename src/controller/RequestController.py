from flask import Flask, request
from Util.JobUtil import JobUtil
from Util.FileUtil import FileUtil
from Util.WordCloudUtil import WordCloudUtil
from flask_cors import *
from Util.JsonUtil import JsonUtil
import json

app = Flask(__name__)
# 解决跨域请求资源被拦截问题
CORS(app, supports_credentials=True, resources=r"/*")


@app.route('/search', methods=['POST'])
def search():
    # 获取搜索框的内容
    searchContent = request.values.get("searchContent")
    # 获取省文本
    province = request.values.get("province")
    # 获市文本
    city = request.values.get("city")
    # 拼接要爬取数据的URL
    url = JsonUtil.getUrlSettingProValueByKey("url") + "?key=" + searchContent + "&dqs=010&pageSize=80"
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
    jsonObj = json.loads(jsonData)
    jsonstr = JsonUtil.jsonListToViewJson(jsonObj)
    print(jsonstr)
    # 产生词云图片保存到指定的文件路径中
    WordCloudUtil.wordCould(wordText, bgImgPath, smallImgPath, 0.5)
    return jsonstr


if __name__ == '__main__':
    app.run(debug=True)
