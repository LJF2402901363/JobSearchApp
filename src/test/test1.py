from Util.JobUtil import JobUtil
from Util.FileUtil import FileUtil
from Util.ImageUtil import ImageUtil
from Util.WordCloudUtil import WordCloudUtil
import demjson
if __name__ == '__main__':
    url = "https://www.liepin.com/zhaopin/?key=Java&dqs=010&pageSize=80"
    jobList = JobUtil.getJobList(url)
    wordText = ""
    for jobInfo in jobList:
        wordText = wordText + jobInfo.jobDes
        # jobInfo.printJobInfo()
    # print(wordText)
    jsonDataStr =demjson.encode(jobList)
    print(jsonDataStr)
    fileName = "../webapp/file/wordText.txt"
    FileUtil.saveTextToFile(text=wordText, filePath=fileName)
    wordText = FileUtil.readFileToTex(fileName)
    smallImgPath = "../webapp/img/small.jpg"
    bgImgPath = '../webapp/img/wordCloudBg.png'
    WordCloudUtil.wordCould(wordText, bgImgPath, smallImgPath, 0.5)
    bigImgPath = "../webapp/img/big.jpg"
    ImageUtil.imageScale(smallImgPath,bigImgPath,2,2)

