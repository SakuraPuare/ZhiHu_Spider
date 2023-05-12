import json
import pathlib

import httpx
from selenium import webdriver
from sqlalchemy import distinct
from tqdm import tqdm

from connection import API
from database import *

httpx_cookies = httpx.Cookies()
cookies_path = pathlib.Path('cookies.json')
api = API()


def get_cookies() -> None:
    global httpx_cookies
    if cookies_path.exists():
        with open(cookies_path, 'r') as f:
            cookies = json.load(f)
    else:
        driver = webdriver.Chrome()
        driver.get('https://www.zhihu.com/signin?next=%2F')
        while True:
            if driver.current_url == 'https://www.zhihu.com/':
                break
        cookies = driver.get_cookies()
        with open(cookies_path, 'w') as f:
            json.dump(cookies, f, ensure_ascii=False)
    for cookie in cookies:
        httpx_cookies.set(cookie.get('name'), cookie.get('value'), domain=cookie.get('domain'))


def get_topic(topic_id: int) -> None:
    info = api.get_topic(topic_id, '', httpx_cookies, arg={'include': 'created,updated'}, types='v4').json()
    db.inserts(zhihu_topic.load(info))

    num = api.get_topic(topic_id, '/feeds/essence', httpx_cookies, arg={'limit': 1}).json().get('paging', {}).get(
        'totals', 0)
    for i in range(0, num, 20):
        data = api.get_topic(topic_id, '/feeds/essence', httpx_cookies, {'limit': 20, 'offset': i}, types='v4').json()
        if not data.get('data', None):
            break
        data = data.get('data')
        answer_list = []
        article_list = []
        user_list = []
        quesiton_list = []
        for j in data:
            target = j.get('target')
            user_list.append(target.get('author'))
            types = target.get('type')
            if types == 'answer':
                quesiton_list.append(target.get('question'))
                answer_list.append(target)
            elif types == 'article':
                article_list.append(target)

        if answer_list:
            db.inserts([zhihu_answer.load(i) for i in answer_list])
        if article_list:
            db.inserts([zhihu_article.load(i) for i in article_list])
        if user_list:
            db.inserts([zhihu_user.load(i) for i in user_list])
        if quesiton_list:
            db.inserts([zhihu_question.load(i) for i in quesiton_list])


def get_question_answer(question_id: int) -> None:
    num = api.get_question(question_id, '/answers', httpx_cookies, arg={'limit': 1}).json().get('paging', {}).get(
        'totals', 0)
    for j in range(0, num, 20):
        arg = {'limit': 20,
               'offset': j,
               'include': 'content,voteup_count,favlists_count,comment_count,is_labeled'
               }
        data = api.get_question(question_id, '/answers', httpx_cookies, arg=arg).json()
        if not data.get('data', None):
            break
        data = data.get('data')
        answer_list = []
        user_list = []
        for k in data:
            user_list.append(k.get('author'))
            answer_list.append(k)

        if answer_list:
            db.inserts([zhihu_answer.load(i) for i in answer_list])
        if user_list:
            db.inserts([zhihu_user.load(i) for i in user_list])


def get_answer_comment(answer_id: int) -> None:
    num = api.get_answer(answer_id, '/comments', httpx_cookies, arg={'limit': 1}).json().get('paging', {}).get(
        'totals', 0)
    for j in range(0, num, 20):
        arg = {'limit': 20, 'offset': j}
        data = api.get_answer(answer_id, '/comments', httpx_cookies, arg=arg).json()
        if not data.get('data', None):
            break
        data = data.get('data')
        comment_list = []
        user_list = []
        for k in data:
            user_list.append(k.get('author', {}).get('member', {}))
            comment_list.append(k)

        if comment_list:
            db.inserts([zhihu_comment.load(i) for i in comment_list])
        if user_list:
            db.inserts([zhihu_user.load(i) for i in user_list])


def get_question_comment(question_id: int) -> None:
    num = api.get_question(question_id, '/comments', httpx_cookies, arg={'limit': 1}).json().get('paging', {}).get(
        'totals',
        0)
    for j in range(0, num, 20):
        arg = {'limit': 20, 'offset': j}
        data = api.get_question(question_id, '/comments', httpx_cookies, arg=arg).json()
        if not data.get('data', None):
            break
        data = data.get('data')
        comment_list = []
        user_list = []
        for k in data:
            user_list.append(k.get('author', {}).get('member', {}))
            comment_list.append(k)

        if comment_list:
            db.inserts([zhihu_comment.load(i) for i in comment_list])
        if user_list:
            db.inserts([zhihu_user.load(i) for i in user_list])


def get_article_comment(article_id: int) -> None:
    num = api.get_article(article_id, '/comments', httpx_cookies, arg={'limit': 1}).json().get('paging', {}).get(
        'totals', 0)
    for j in range(0, num, 20):
        arg = {'limit': 20, 'offset': j}
        data = api.get_article(article_id, '/comments', httpx_cookies, arg=arg).json()
        if not data.get('data', None):
            break
        data = data.get('data')
        comment_list = []
        user_list = []
        for k in data:
            user_list.append(k.get('author', {}).get('member', {}))
            comment_list.append(k)

        if comment_list:
            db.inserts([zhihu_comment.load(i) for i in comment_list])
        if user_list:
            db.inserts([zhihu_user.load(i) for i in user_list])


def get_all_topic() -> None:
    topic_list = []
    bar = tqdm(topic_list)
    for topic in bar:
        get_topic(topic)


def get_all_question_answer() -> None:
    question_list = [i[0] for i in db.session.query(distinct(zhihu_question.uid)).all()]
    bar = tqdm(question_list)
    for question in bar:
        bar.set_description(f'{question}')
        get_question_answer(question)


def get_all_answer_comment() -> None:
    answer_list = [i[0] for i in db.session.query(distinct(zhihu_answer.uid)).all()]
    bar = tqdm(answer_list)
    for answer in bar:
        bar.set_description(f'{answer}')
        get_answer_comment(answer)


def get_all_question_comment() -> None:
    question_list = [i[0] for i in db.session.query(distinct(zhihu_question.uid)).all()]
    bar = tqdm(question_list)
    for question in bar:
        bar.set_description(f'{question}')
        get_question_comment(question)


def get_all_article_comment() -> None:
    article_list = [i[0] for i in db.session.query(distinct(zhihu_article.uid)).all()]
    bar = tqdm(article_list)
    for article in bar:
        bar.set_description(f'{article}')
        get_article_comment(article)


def main():
    get_all_topic()
    get_all_question_answer()
    get_all_answer_comment()
    get_all_question_comment()
    get_all_article_comment()


if __name__ == '__main__':
    get_cookies()

    db = Database('mysql+pymysql://root:20131114@localhost:3306/env?charset=utf8mb4')
    db.create_all_table()

    main()
    pass
