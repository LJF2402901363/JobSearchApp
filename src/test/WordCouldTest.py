# -*- coding: utf-8 -*-
from wordcloud import WordCloud

if __name__ == '__main__':
    text = "I love you;you love me"
    wc = WordCloud(
        background_color='white',
        width=600,
        height=300,  # 图片高度
        max_font_size=100,  # 字体最大值
        random_state=100,  # 配色方案的种类
    )
    wc.generate(text)
    wc.to_file("test.png")