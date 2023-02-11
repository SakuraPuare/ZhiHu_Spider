import asyncio
import json
import pathlib
from typing import Union
from urllib.parse import urlencode

import httpx
import tqdm

from database import SQL, Answer, User

cookies_path = pathlib.Path('cookies.json')

topic_id = 25850855

sql = SQL()


# driver = webdriver.Chrome()


def read_cookies(path: pathlib.Path = pathlib.Path('cookies.json')) -> dict:
    with open(path, 'r') as f:
        cookies = json.load(f)
        return cookies


def save_cookies(path: pathlib.Path = pathlib.Path('cookies.json')) -> None:
    cookies = driver.get_cookies()
    with open(path, 'w') as f:
        json.dump(cookies, f, ensure_ascii=False)


def get_cookies() -> httpx.Cookies:
    httpx_cookies = httpx.Cookies()
    if cookies_path.exists():
        cookies = read_cookies()
    else:
        cookies = driver.get_cookies()
    for cookie in cookies:
        httpx_cookies.set(cookie.get('name'), cookie.get('value'), domain=cookie.get('domain'))
    return httpx_cookies


async def get(msg: str, kwarg: Union[dict, str] = '') -> dict:
    async with httpx.AsyncClient(cookies=get_cookies()) as client:
        url = f'https://api.zhihu.com/' + msg + kwarg
        request = await client.get(url=url, follow_redirects=True)
        assert request.status_code == 200
        return request.json()


async def get_topic(ids: int, types: str = '') -> dict:
    msg = f'topics/{ids}' + types
    return await get(msg)


async def get_api(ids: int, where: str, types: str = '') -> dict:
    msg = f'{where}/{ids}' + types
    return await get(msg)


async def main():
    # 获取话题信息
    # topic = await get_topic(topic_id)
    # sql.insert_into('topic', Topic, topic)
    #
    # # 获取话题精华
    # num = await get_topic(topic_id, '/feeds/essence?offset=0&limit=1')
    # num = num.get('paging').get('totals')
    #
    # for i in tqdm.tqdm(range(0, num, 50)):
    #     params = {'offset': i, 'limit': 50}
    #     urlencode(params)
    #     data = await get_topic(topic_id, f'/feeds/essence?{urlencode(params)}')
    #     if not (data and data.get('data')):
    #         continue
    #     data = [i for i in data.get('data')]
    #     answer_list = []
    #     article_list = []
    #     user_list = []
    #     quesiton_list = []
    #     for j in data:
    #         target = j.get('target')
    #         user_list.append(target.get('author'))
    #         types = target.get('type')
    #         if types == 'answer':
    #             quesiton_list.append(target.get('question'))
    #             answer_list.append(target)
    #         elif types == 'article':
    #             article_list.append(target)
    #     if answer_list:
    #         sql.insert_into('answer', Answer, answer_list)
    #         pass
    #     if article_list:
    #         sql.insert_into('article', Article, article_list)
    #         pass
    #     if user_list:
    #         sql.insert_into('user', User, user_list)
    #         pass
    #     if quesiton_list:
    #         sql.insert_into('question', Question, quesiton_list)
    #         pass
    #     # time.sleep(0.5)

    # 获取所有回答
    sql._execute('select * from answer order by id')
    data = sql.cursor.fetchall()
    bar = tqdm.tqdm(data)
    for answer in bar:
        answer_id = answer[1]
        # 获取回答评论
        num = (await get_comment(answer_id, 'answers', '/comments')).get('paging', {}).get('totals', 0)
        bar.set_description(f'answer_id: {answer_id} num: {num}')
        user_list = []
        comment_list = []
        for i in range(0, num, 20):
            params = {'offset': i, 'limit': 20}
            urlencode(params)
            data = await get_comment(answer_id, f'/comments?{urlencode(params)}')
            if not (data and data.get('data')):
                continue
            comment_list.extend(data.get('data'))
            user_list.extend([i.get('author').get('member') for i in data.get('data')])
            user_list.extend(
                [i.get('reply_to_author').get('member') for i in data.get('data') if i.get('reply_to_author', None)])
        if comment_list:
            sql.insert_into('comment', Comment, comment_list)
        if user_list:
            sql.insert_into('user', User, user_list)
        time.sleep(1)

    # for quesion in bar:
    #     quesion_id = quesion[1]
    #     # 获取回答
    #     num = (await get_comment(quesion_id, 'questions', '/comments?offset=0&limit=1')).get('paging', {}).get('totals',
    #                                                                                                            0)
    #     bar.set_description(f'quesion_id: {quesion_id} num: {num}')
    #     user_list = []
    #     answer_list = []
    #     for i in range(0, num, 20):
    #         params = {'offset': i, 'limit': 20}
    #         urlencode(params)
    #         data = await get_comment(quesion_id, f'/comments?{urlencode(params)}')
    #         if not (data and data.get('data')):
    #             continue
    #         answer_list.extend(data.get('data'))
    #         user_list.extend([i.get('author').get('member') for i in data.get('data')])
    #     if answer_list:
    #         sql.insert_into('answer', Answer, answer_list)
    #     if user_list:
    #         sql.insert_into('user', User, user_list)
    #     # time.sleep(0.5)


    pass


if __name__ == '__main__':
    # driver.get('https://www.zhihu.com/signin')
    # # 加载cookies
    # if cookies_path.exists():
    #     cookies = read_cookies()
    #     for cookie in cookies:
    #         driver.add_cookie(cookie)
    # else:
    #     driver.refresh()
    #     driver.implicitly_wait(10)
    #     while driver.current_url != 'https://www.zhihu.com/':
    #         time.sleep(0.5)
    #     save_cookies()

    asyncio.run(main())
