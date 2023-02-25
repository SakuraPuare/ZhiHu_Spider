import random

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from wordcloud import WordCloud

data = """霍乱	1458
传染病	1034
病例	980
传播	809
出现	782
美国	775
霍乱弧菌	736
腹泻	729
武汉	686
感染	651
新冠	565
症状	455
甲类	446
污染	445
治疗	441
预防	435
武汉大学	426
食物	426
宿舍	422
病毒	404
患者	398
疾病	370
死亡	355
问题	353
检测	352
引起	349
肠道	343
中国	325
呕吐	321
发现	308
流行	306
疫情	303
"""


def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    # 返回灰黑色
    return "hsl(0, 0%%, %d%%)" % random.randint(10, 50)


data = {i.split()[0]: int(i.split()[1]) for i in data.split('\n') if i}

font_path = 'D:/Downloads/SourceHanSerifSC-VF.otf'
mask = np.array(Image.open('C:/Users/SakuraPuare/Desktop/Vibrio-cholerae-Food-Poisoning.png'))

wc = WordCloud(font_path=font_path, background_color=None, mode="RGBA", max_words=2000, mask=mask,
               max_font_size=150, random_state=50, width=3000, height=4000, margin=2,scale=1.2)

wc.generate_from_frequencies(data)

plt.figure()

# 调整图像大小
plt.figure(figsize=(30, 40), dpi=100)

# 背景颜色
plt.rcParams['figure.facecolor'] = 'black'

# recolor wordcloud and show
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
wc.to_file('wordcloud.png')
plt.show()

# save wordcloud
