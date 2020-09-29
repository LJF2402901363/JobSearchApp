## 1.本项目基于Python作为爬虫技术，使用flask作为web项目的开发框架。

## 2.本项目预期实现的功能有：

### 	2.1简单的web页面展示，将需要搜索的结果使用词云，饼状图，柱状图这三种形式表现出来。

## 	2.2输入关键字后搜索后能根据搜索结果智能推荐最合适的职位。

### 	2.3支持多条件复杂查询，结合行业，所选城市进行综合查询。

### 	2.4通过手动添加新词进行过滤词云内容达到更加精确人性化的结果。

## 3.使用的技术有：

### 	3.1前端

####     	 3.1.1页面：HTML+CSS+JavaScript+JQuery

#### 		 3.1.2前端框架：boostrap 

#### 		 3.1.3前端插件： echarts（用于将结果渲染程柱状图和饼状图）+dispicker(显示省市区便于选择地区) + smart-zoom（将词云图进行放大）

### 	3.2后端

#### 		 3.2.1 基于flask的web框架

#### 		 3.2.2jieba用于处理分析搜索到的岗位要求以及描述然后利用wordcloud进行生成词云

#### 		 3.2.3使用BeautifulSoup对获取的网站源代码进行提取想要的内容。

​			

## 4.目前实现的功能

#### 	4.1通过关键字搜索获取文本后经过处理生成词云然后在页面中显示出词云以及对应数据的柱状图和饼状图直观看到不同要求的差异。

#### 	4.2已在页面中写好省市区的视图页面但是查询**<u>尚未支持地区查询。**</u>

#### 	4.3本项目的图片URL，文件的URL，词云图片的URL，过滤词组，添加的新词组，每个爬取标签的唯一选择器selector文本均已经写成json格式的配置文件放在项目中。当项目启动时会自动加载这些数据，并且支持实时更新这些json配置信息的内容而对不需要重新启动项目。

## 5.配置文件

### 5.1urlSettingPro.json的配置

  ![image-20200929002344070](readMeImages/image-1.png)

配置项的含义：

```
   "url":需要爬取的网站URL
   "jobInfoLinkDiv":job详细信息的链接的selector。
   "jobNameDiv":工作名称标签的selector，由于是动态的所以可能导致不同的job的信息源代码中jobName标签的selector有对个，那么就配置多项。如下内容均是一样。
    "jobCompanyNameDiv": {"name1": "div.title-info > h3 a"},
   "jobSalaryDiv": 源码中工作薪水的选择器，有多个就配置多个
  "jobQualificationsDiv":源码中多个要求的标签的选择器
  "jobDesDiv": 源码中工作描述或者要求的选择器
  "jobAgeDiv":源码中年龄标签的选择器
  
```

比如：在某一个工作中，

![image-20200929001712586](readMeImages/image-2.png)

jobDesDiv的标签的selector在源代码中的位置为：

![image-20200929001449142](readMeImages/image-3.png)

“div.job-main.job-description.main-message > div”能够唯一确定其位置。

但是在另一个工作页面中![image-20200929001833201](readMeImages/image-4.png)

它在源码中的选择器selector就是另外一个了：

![image-20200929001814181](readMeImages/image-5.png)

因此jobDesDiv就有两个选择器selector，那么它的配置方法就是：

 "jobDesDiv": {
    "name1":"div.job-item.main-message.job-description > div",
    "name2": "div.job-main.job-description.main-message > div"
  }

### 5.2fileAndImgPro.json的配置

```
{

   "wordCloudImg_small":"static/img/small.jpg",
   "wordCloudBgImg":"static/img/wordCloudBg.png",
   "ignoreWords":"[\",\"\".\"\"。\"\"?\"\"？\"\"’\"\"‘\"\"'\"\"”\"\"“\"\"【\"\"】\"\"{\"\"}\"\"｛\"\"｝\"\"：\"\":\"\"、\"\"任职要求\"\"任职要求1\"\"职位描述\"\"职位描述1\"\"岗位职责\"\"工作职责\"\\d]",
   "textFilePath": "static/file/wordText.txt",
   "newWords": "[{\"word\":\"天天学习\",\"freq\":4},{\"word\":\"机器学习\",  \"freq\":3},{\"word\":\"数据挖掘\",\"freq\":5},{\"word\":\"熟悉算法\",\"freq\":4}]"
}
```

**wordCloudImg_small**：前端页面中词云图片的URL地址

**wordCloudBgImg**：在生成词云时的背景图片的URL

**ignoreWords**：在岗位描述或者岗位要求职责中需要过滤的词语或符号，该表达式必须是 **<u>正则表达式</u>**

newWords：在jieba库进行精确拆分提取文本内容得到每个词语的出现频率时，手动添加新的词语使得jieba在分析时识别出文本中含有的这个词语不被拆分。使用json数据格式进行添加，其中，｛“word”: 词语,"freq": 正整数值｝是一个json对象，word对应的是添加的词语，freq对应的是出现的频率。

**textFilePath**：从网站爬取的职位职责要求描述文本保存到该路径的文本文件下。



## 6.效果图

![image-20200929102739670](readMeImages/image-6.png)

![image-20200929102753667](readMeImages/image-7.png)

