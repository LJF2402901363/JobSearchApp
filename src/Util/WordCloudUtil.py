# 导入需要模块
import jieba
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import json


class WordCloudUtil:
    @staticmethod
    def wordCould(text, backGroudImgPath, desPath, scale):
        """
         对给定的text文本以backGroudImgPath的图片为背景图片并按照指定的缩放比例scale生成词云，然后写入到desPath路径中去
        :param text: 给定的文本
        :param backGroudImgPath:背景图片路径
        :param desPath: 词云图片存储的目的地
        :param scale: 图片的缩放比
        :return: null
        """
        # 加载背景图
        color_mask = np.array(Image.open(backGroudImgPath))
        wc1 = WordCloud(
            scale=scale,  # 图片的缩放比例
            mask=color_mask,  # 背景图颜色
            background_color='white',  # 背景颜色
            height=300,  # 图片高度
            width=500,  # 图片宽度
            max_font_size=100,  # 字体最大值
            random_state=100,  # 配色方案的种类
            font_path="static/font/AdobeHeitiStd-Regular.otf",  # 不加这一句显示口字形乱码
        )
        # 产生词云
        wc1.generate(text)
        # 在只设置mask的情况下 会得到一个拥有图片形状的词云 axis默认为on 会开启边框
        plt.imshow(wc1, interpolation="bilinear")
        plt.axis("off")
        # 将图片保存到指定的目录文件中去
        plt.savefig(desPath)

    @staticmethod
    def getWordCouldJson(text,wordJson):
        """
        将给定的文本进心分词处理，并且添加json格式的新词，在分词过程中wordJSon中的词语不被切分，返回一个json数组
        [
        {
        "name": name,
        "value":value
        },
        {
        "name": name,
        "value":value
        }
        ]
        :param text:需要进行分词的文本
        :param wordJson:在分词过程中不被切分的词语的json数组
        :return:返回分词一个分词和对应出现频率的json对象数组
        """
        for word in wordJson:
            jieba.add_word(word['word'],word['freq'])
        words = jieba.cut(text)  # 使用精确模式对文本进行分词
        counts = {}  # 通过键值对的形式存储词语及其出现的次数
        # 统计词频
        for word in words:
            if len(word) == 1:  # 单个词语不计算在内
                continue
            else:
                counts[word] = counts.get(word, 0) + 1  # 遍历所有词语，每出现一次其对应的值加 1
        # 注解：dict.get(word,0)当能查询到相匹配的字典时，就会显示相应key对应的value，如果不能的话，就会显示后面的这个参数
        # 有些不重要的词语但出现次数较多，可以通过构建排除词库excludes来删除
        items = list(counts.items())
        # 根据词语出现的次数进行从大到小排序
        items.sort(key=lambda x: x[1], reverse=True)
        dictList = {}
        for item in items:
            dictList[item[0]] = item[1]
        # 将字典转换为json对象
        return json.dumps(dictList,ensure_ascii=False)
