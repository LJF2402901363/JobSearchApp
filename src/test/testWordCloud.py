import jieba as  jb
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from src.Util.FileUtil import FileUtil
import json


txt = FileUtil.readFileToTex("E:\\flaskProject\\static\\file\wordText.txt",'["岗位职责""工作描述""工作职责""工作职责1""要求"]')
print(txt)
jb.add_word("机器学习",4)
words = jb.cut(txt)  # 使用精确模式对文本进行分词
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

items.sort(key=lambda x: x[1], reverse=True)  # 根据词语出现的次数进行从大到小排序
jsonData = json.dumps(items,ensure_ascii=False)
print(jsonData)
# 输出统计结果
for i in range(10):
    word, count = items[i]
    print("{0:<10}{1:>10}".format(word, count))

# 绘图
wc = WordCloud(background_color='white',  # 设置背景颜色
               font_path='msyh.ttc',  # 若是有中文的话，这句代码必须添加，不然会出现方框，不出现汉字
               scale=2,  # 按照比例进行放大画布，如设置为2，则长和宽都是原来画布的1.5倍
               max_words=100,  # 设置最大现实的字数
               max_font_size=80,  # 设置字体最大值
               # stopwords=excludes  # 设置停用词
               )

wc.generate(txt)

# 显示词云图
plt.imshow(wc)
plt.axis('off')
plt.show()
wc.to_file(r'E:\\flaskProject\\static\\file\三国演义.jpg')
