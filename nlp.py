import tqdm
from paddlenlp import Taskflow

from database import *

# Define the schema for sentence-level sentiment classification
schema = '关键词'
ie = Taskflow('information_extraction', schema=schema, model='uie-base', device_id='cpu')
ie.set_schema(schema)
sql = SQL()

content_list = []


content_list.extend([i[4] for i in sql.fetchall("SELECT * FROM comment")])
content_list.extend([i[12] for i in sql.fetchall("SELECT * FROM answer")])
content_list.extend([i[12] for i in sql.fetchall("SELECT * FROM article")])

data = []

bar = tqdm.tqdm(content_list)
for num, i in enumerate(content_list):
    bar.update(1)
    bar.set_description(f"Progress: {num / len(content_list) * 100:.2f}%")
    resp = ie(i)
    if resp[0]:
        data.append(resp)
    pass
