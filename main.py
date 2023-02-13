import json
import pathlib

import httpx
import tqdm

from connection import API
from database import *
from selenium import webdriver

cookies_path = pathlib.Path('cookies.json')

httpx_cookies = httpx.Cookies()

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


def topic(ids: int) -> None:
    info = api.get_topic(ids, '', httpx_cookies, arg={'include': 'created,updated'}, types='v4').json()
    sql.insert_into('topic', Topic, [info])

    num = api.get_topic(ids, '/feeds/essence', httpx_cookies, arg={'limit': 1}).json().get('paging', {}).get('totals',
                                                                                                             0)
    for i in range(0, num, 20):
        data = api.get_topic(ids, '/feeds/essence', httpx_cookies, {'limit': 20, 'offset': i}, types='v4').json()
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
            sql.insert_into('answer', Answer, answer_list)
        if article_list:
            sql.insert_into('article', Article, article_list)
        if user_list:
            sql.insert_into('user', User, user_list)
        if quesiton_list:
            sql.insert_into('question', Question, quesiton_list)
        pass


def article(ids: int) -> None:
    if sql.execute(f'select * from article where uid={ids}'):
        return
    resp = api.get_article(ids, '', httpx_cookies, arg={'include': 'created,updated'}, types='v4').json()
    user = resp.get('author')
    sql.insert_into('user', User, [user])
    sql.insert_into('article', Article, [resp])
    pass


def answer(ids: int) -> None:
    if sql.execute(f'select * from answer where uid={ids}'):
        return
    resp = api.get_answer(ids, '', httpx_cookies,
                          arg={'include': 'content,voteup_count,favlists_count,comment_count'}).json()
    user = resp.get('author')
    sql.insert_into('user', User, [user])
    sql.insert_into('answer', Answer, [resp])
    pass


def video(ids: int) -> None:
    video = ['1529880790133026817', '1529833914981576704', '1529962723954094080', '1529967315055910912',
             '1529849912804483072', '1530187358909968384', '1530298859439431680', '1532388641251164162',
             '1530232119959343104', '1529754085816844288', '1529762804852109312', '1533884804688408576',
             '1529941589467766784', '1530189496443854848', '1530238563434532864', '1529888295286239232']
    pass


def serch(s: str) -> None:
    soup = BeautifulSoup(s, 'html.parser')
    links = [i.attrs['href'] for i in soup.find_all('a', href=True)]

    article_list = set([i.split('/')[-1] for i in links if 'zhuanlan' in i])
    answer_list = set([i.split('answer/')[-1] for i in links if 'answer' in i and 'question' in i])
    video_list = set([i.split('zvideo/')[-1] for i in links if 'video' in i])

    # [article(i) for i in article_list]
    # [answer(i) for i in answer_list]
    [video(i) for i in video_list]

    pass


def main():
    # 获取话题所有信息
    # topic_list = [25850855, 25850506, 25851254, 25850213, 25850511, 25861011, 25868391, 25848648, 25873490]
    # [topic(i) for i in tqdm.tqdm(topic_list)]

    # 从html中进行搜索
    with open('a.html', 'r', encoding='utf-8') as f:
        serch(f.read())

    # 获取问题所有回答
    # question_list = sql.fetchall(f'select * from question')
    # bar = tqdm.tqdm(question_list)
    # for i in bar:
    #     uid = i[1]
    #     num = api.get_question(uid, '/answers', httpx_cookies, arg={'limit': 1}).json().get('paging', {}).get('totals',
    #                                                                                                           0)
    #     bar.set_description(f'question: {uid}, num: {num}')
    #     for j in range(0, num, 20):
    #         arg = {'limit': 20,
    #                'offset': j,
    #                'include': 'content,voteup_count,favlists_count,comment_count,is_labeled'
    #                }
    #         data = api.get_question(uid, '/answers', httpx_cookies, arg=arg).json()
    #         if not data.get('data', None):
    #             break
    #         data = data.get('data')
    #         answer_list = []
    #         user_list = []
    #         for k in data:
    #             user_list.append(k.get('author'))
    #             answer_list.append(k)
    #
    #         if answer_list:
    #             sql.insert_into('answer', Answer, answer_list)
    #         if user_list:
    #             sql.insert_into('user', User, user_list)

    # 获取回答所有评论
    # answer_list = sql.fetchall(f'select * from answer')
    # bar = tqdm.tqdm(answer_list)
    # for i in bar:
    #     uid = i[1]
    #     num = api.get_answer(uid, '/comments', httpx_cookies, arg={'limit': 1}).json().get('paging', {}).get('totals',
    #                                                                                                          0)
    #     bar.set_description(f'answer: {uid}, num: {num}')
    #     for j in range(0, num, 20):
    #         arg = {'limit': 20, 'offset': j}
    #         data = api.get_answer(uid, '/comments', httpx_cookies, arg=arg).json()
    #         if not data.get('data', None):
    #             break
    #         data = data.get('data')
    #         comment_list = []
    #         user_list = []
    #         for k in data:
    #             user_list.append(k.get('author', {}).get('member', {}))
    #             comment_list.append(k)
    #
    #         if comment_list:
    #             sql.insert_into('comment', Comment, comment_list)
    #         if user_list:
    #             sql.insert_into('user', User, user_list)

    # 获取问题所有评论
    # question_list = sql.fetchall(f'select * from question')
    # bar = tqdm.tqdm(question_list)
    # for i in bar:
    #     uid = i[1]
    #     num = api.get_question(uid, '/comments', httpx_cookies, arg={'limit': 1}).json().get('paging', {}).get('totals',
    #                                                                                                           0)
    #     bar.set_description(f'question: {uid}, num: {num}')
    #     for j in range(0, num, 20):
    #         arg = {'limit': 20, 'offset': j}
    #         data = api.get_question(uid, '/comments', httpx_cookies, arg=arg).json()
    #         if not data.get('data', None):
    #             break
    #         data = data.get('data')
    #         comment_list = []
    #         user_list = []
    #         for k in data:
    #             user_list.append(k.get('author', {}).get('member', {}))
    #             comment_list.append(k)
    #
    #         if comment_list:
    #             sql.insert_into('comment', Comment, comment_list)
    #         if user_list:
    #             sql.insert_into('user', User, user_list)

    # 获取文章所有评论
    # article_list = sql.fetchall(f'select * from article')
    # bar = tqdm.tqdm(article_list)
    # for i in bar:
    #     uid = i[1]
    #     num = api.get_article(uid, '/comments', httpx_cookies, arg={'limit': 1}).json().get('paging', {}).get('totals',
    #                                                                                                             0)
    #     bar.set_description(f'article: {uid}, num: {num}')
    #     for j in range(0, num, 20):
    #         arg = {'limit': 20, 'offset': j}
    #         data = api.get_article(uid, '/comments', httpx_cookies, arg=arg).json()
    #         if not data.get('data', None):
    #             break
    #         data = data.get('data')
    #         comment_list = []
    #         user_list = []
    #         for k in data:
    #             user_list.append(k.get('author', {}).get('member', {}))
    #             comment_list.append(k)
    #
    #         if comment_list:
    #             sql.insert_into('comment', Comment, comment_list)
    #         if user_list:
    #             sql.insert_into('user', User, user_list)
    pass


if __name__ == '__main__':
    # 设置cookies
    # get_cookies()
    # # 建立sql连接
    # sql = SQL()
    # 运行
    main()
