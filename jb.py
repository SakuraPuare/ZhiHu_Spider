import jieba.analyse
from tqdm import tqdm

from database import *

sql = SQL()

data = [i[12] for i in sql.fetchall('select * from answer order by id;')]
data.extend([i[12] for i in sql.fetchall('select * from article order by id;')])
data.extend([i[10] for i in sql.fetchall('select * from article order by id;')])
data.extend([i[4] for i in sql.fetchall('select * from comment order by id;')])
data.extend([i[3] for i in sql.fetchall('select * from question order by id;')])
data.extend([i[2] for i in sql.fetchall('select * from topic order by id;')])

bar = tqdm(data)
resp = []
for i in bar:
    resp.extend(jieba.analyse.extract_tags(i, topK=50))
    resp.extend(jieba.analyse.textrank(i, topK=50))

# 去重
resp_set = set(resp)

# 排序
resp_set = sorted(resp_set, key=lambda x: resp.count(x), reverse=True)

# 记录到csv文件
with open('all_word.csv', 'w', encoding='gbk') as f:
    f.write('word,times\n')
    for i in resp_set:
        f.write('{},{}\n'.format(i.replace(',', '，'), resp.count(i)))
