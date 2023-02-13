from snownlp import SnowNLP
from tqdm import tqdm

from database import *

sql = SQL()

content_list = []
content_list.extend([i[12] for i in sql.fetchall('select * from answer order by id;')])
content_list.extend([i[12] for i in sql.fetchall('select * from article order by id;')])
content_list.extend([i[10] for i in sql.fetchall('select * from article order by id;')])
content_list.extend([i[4] for i in sql.fetchall('select * from comment order by id;')])
content_list.extend([i[3] for i in sql.fetchall('select * from question order by id;')])
content_list.extend([i[2] for i in sql.fetchall('select * from topic order by id;')])

bar = tqdm(content_list)
data_list = []

word_list = []


def get_set(x):
    return 'positive' if x > 0.66 else 'negative' if x < 0.33 else 'neutral'


for i in bar:
    bar.set_description(f"Progress: {bar.n / len(content_list) * 100:.2f}%")
    try:
        snow = SnowNLP(i)
        sentiment = snow.sentiments
        data = (i, get_set(sentiment), sentiment)
        data_list.append(data)

        # 分词
        words = snow.words
        word_list.extend(words)
    except:
        continue

# 记录到csv文件
with open('snow_sentiment.csv', 'w', encoding='u8') as f:
    f.write('content,type,sentiment\n')
    for i in data_list:
        f.write('"{0}","{1}",{2}\n'.format(i[0].replace('"', "'").replace(',', '，'), i[1], i[2]))

# word去重
word_set = set(word_list)
# 排序
word_set = sorted(word_set, key=lambda x: word_list.count(x), reverse=True)
# 记录到csv文件
with open('snow_word.csv', 'w', encoding='u8') as f:
    f.write('word,times\n')
    for i in word_set:
        f.write('{},{}\n'.format(i.replace(',', '，'), word_list.count(i)))
