from paddlenlp import Taskflow
from tqdm import tqdm

from database import *

sql = SQL()
schema = '情感倾向[积极，中立，消极]'
task = Taskflow('information_extraction', model='uie-base', schema=schema)


def f(x):
    return 50 * x


data_list = []
data_list.extend([i[12] for i in sql.fetchall("SELECT * FROM answer;")])
data_list.extend([i[10] for i in sql.fetchall("SELECT * FROM article;")])
data_list.extend([i[12] for i in sql.fetchall("SELECT * FROM article;")])
data_list.extend([i[3] for i in sql.fetchall("SELECT * FROM comment;")])
data_list.extend([i[3] for i in sql.fetchall("SELECT * FROM question;")])
data_list.extend([i[2] for i in sql.fetchall("SELECT * FROM topic;")])

bar = tqdm(data_list[1797+179:])
for data in bar:
    bar.set_description("Processing %s" % data[:5])
    try:
        result = task(data)
    except:
        sql.execute(f'insert into emotion_ (content,type,probability,score) values ("{data}","无","0","0");')
        continue
    if not result and not result[0]:
        sql.execute(f'insert into emotion_ (content,type,probability,score) values ("{data}","无","0","0");')
        continue
    result = result[0].get(schema, None)
    if not result:
        sql.execute(f'insert into emotion_ (content,type,probability,score) values ("{data}","无","0","0");')
        continue
    text = result[0].get('text')
    probability = result[0].get('probability')
    score = f(probability)
    sql.execute(
        f'insert into emotion_ (content,type,probability,score) values ("{data}","{text}","{probability}","{score}");')
    # print(result)
