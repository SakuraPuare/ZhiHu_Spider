import re

import thulac
from tqdm import tqdm

from database import *

sql = SQL()

data = sql.fetchall('select * from answer order by id;')
bar = tqdm(data)

word_list = []
thu = thulac.thulac(user_dict='user_dict.txt')
for item in bar:
    content = item[12]
    # 移除表情
    content = re.sub(r'\[.*?\]', '', content)
    # 移除标点符号
    content = re.sub(r'[^\w\s]', ' ', content)
    # 移除unicode特殊字符
    content = re.sub(r'\\u[0-9a-fA-F]{4}', '', content)
    # 移除链接
    content = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', content)
    # 分词
    words = thu.cut(content)
    word_list.extend(words)


data = sql.fetchall('select * from article order by id;')
bar = tqdm(data)


for item in bar:
    content = item[12]
    # 移除表情
    content = re.sub(r'\[.*?\]', '', content)
    # 移除标点符号
    content = re.sub(r'[^\w\s]', ' ', content)
    # 移除unicode特殊字符
    content = re.sub(r'\\u[0-9a-fA-F]{4}', '', content)
    # 移除链接
    content = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', content)
    # 分词
    words = thu.cut(content)
    word_list.extend(words)



data = sql.fetchall('select * from comment order by id;')
bar = tqdm(data)

for item in bar:
    content = item[4]
    # 移除表情
    content = re.sub(r'\[.*?\]', '', content)
    # 移除标点符号
    content = re.sub(r'[^\w\s]', ' ', content)
    # 移除unicode特殊字符
    content = re.sub(r'\\u[0-9a-fA-F]{4}', '', content)
    # 移除链接
    content = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', content)
    # 分词
    words = thu.cut(content)
    word_list.extend(words)

word_type = {}
for i in word_list:
    word_type[i[0]] = i[1]

# 统计词频
words = [i[0] for i in word_list]
words_set = set(words)
words_count = {}
for i in words_set:
    words_count[i] = words.count(i)

type_dict = {
    'n': '名词',
    'np': '人名',
    'ns': '地名',
    'ni': '机构名',
    'nz': '其他专名',
    'm': '数词',
    'q': '量词',
    'mq': '数量词',
    't': '时间词',
    'f': '方位词',
    's': '处所词',
    'v': '动词',
    'a': '形容词',
    'd': '副词',
    'h': '前接成分',
    'k': '后接成分',
    'i': '习语',
    'j': '简称略语',
    'r': '代词',
    'c': '连词',
    'p': '介词',
    'u': '助词',
    'y': '语气词',
    'e': '叹词',
    'o': '拟声词',
    'g': '语素',
    'w': '标点符号',
    'x': '非语素字',
}

# 排序
words_count = sorted(words_count.items(), key=lambda x: x[1], reverse=True)

# 导出到csv
with open('article_word_type.csv', 'w', encoding='utf-8') as f:
    f.write('word,type,count\n')
    for i in words_count:
        f.write(f'{i[0]},{type_dict.get(word_type[i[0]], "")}, {i[1]}\n')
