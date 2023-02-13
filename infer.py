import paddlehub as hub

from database import *

sql = SQL()

content_list = []

data = sql.fetchall("SELECT * FROM comment")
content_list.extend([i[4] for i in data])

data = sql.fetchall("SELECT * FROM answer")
content_list.extend([i[12] for i in data])

data = sql.fetchall("SELECT * FROM article")
content_list.extend([i[12] for i in data])

module = hub.Module(name="emotion_detection_textcnn")

result = module.emotion_classify(texts=content_list)
for i in result:
    text = i['text'].replace('"', "'").replace(',', '，')
    emotion = i['emotion_key']
    positive_probs = i['positive_probs']
    neutral_probs = i['neutral_probs']
    negative_probs = i['negative_probs']
    sql_ = f'insert into emotion (content,type,positive,neutral,negative) values ("{text}","{emotion}","{positive_probs}","{neutral_probs}","{negative_probs}")'
    sql.execute(sql_)
