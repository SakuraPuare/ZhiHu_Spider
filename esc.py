from html import unescape

from bs4 import BeautifulSoup

from database import *

sql = SQL()

answer = Answer()
answer_list = sql.fetchall('select * from %s' % answer.name)
for i in answer_list:
    ids = i[0]
    content = i[10]
    soup = BeautifulSoup(unescape(content), 'html.parser')
    text = soup.get_text().replace('"', "'").strip()
    sql.execute(f'update {answer.name} set content_text = "{text}" where id = {ids}')

article = Article()
article_list = sql.fetchall('select * from %s' % article.name)
for i in article_list:
    ids = i[0]
    content = i[10]
    soup = BeautifulSoup(unescape(content), 'html.parser')
    text = soup.get_text().replace('"', "'").strip()
    sql.execute(f'update {article.name} set content_text = "{text}" where id = {ids}')

comment = Comment()
comment_list = sql.fetchall('select * from %s' % comment.name)
for i in comment_list:
    ids = i[0]
    content = i[3]
    soup = BeautifulSoup(unescape(content), 'html.parser')
    text = soup.get_text().replace('"', "'").strip()
    sql.execute(f'update {comment.name} set content_text = "{text}" where id = {ids}')
