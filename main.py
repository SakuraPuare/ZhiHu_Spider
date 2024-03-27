import asyncio

from sqlalchemy import distinct
from tqdm import tqdm

from connection import API
from database import *
from utils import load_all_cookies, save_cookies

api = API()


async def get_topic(topic_id: int) -> None:
    info = (
        await api.get_topic(topic_id, '', arg={'include': 'created,updated'}, types='v5')).json()
    db.inserts(zhihu_topic.load(info))

    num = (await api.get_topic(topic_id, '/feeds/essence', arg={'limit': 1})).json().get('paging',
                                                                                         {}).get(
        'totals', 0)
    for i in range(0, num, 20):
        data = (await api.get_topic(topic_id, '/feeds/essence', {'limit': 20, 'offset': i},
                                    types='v5')).json()
        if not data.get('data', None):
            break
        data = data.get('data')
        answer_list = []
        article_list = []
        user_list = []
        question_list = []
        for j in data:
            target = j.get('target')
            user_list.append(target.get('author'))
            types = target.get('type')
            if types == 'answer':
                question_list.append(target.get('question'))
                answer_list.append(target)
            elif types == 'article':
                article_list.append(target)

        if answer_list:
            db.inserts([zhihu_answer.load(i) for i in answer_list])
        if article_list:
            db.inserts([zhihu_article.load(i) for i in article_list])
        if user_list:
            db.inserts([zhihu_user.load(i) for i in user_list])
        if question_list:
            db.inserts([zhihu_question.load(i) for i in question_list])


async def get_question_answer(question_id: int) -> None:
    num = (await api.get_question(question_id, '/answers', arg={'limit': 1})).json().get('paging',
                                                                                         {}).get(
        'totals', 0)
    for j in range(0, num, 20):
        arg = {'limit': 20, 'offset': j,
               'include': 'content,voteup_count,favlists_count,comment_count,is_labeled'}
        data = (await api.get_question(question_id, '/answers', arg=arg)).json()
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


async def get_answer_comment(answer_id: int) -> None:
    num = (await api.get_answer(answer_id, '/comments', arg={'limit': 1})).json().get('paging',
                                                                                      {}).get(
        'totals', 0)
    for j in range(0, num, 20):
        arg = {'limit': 20, 'offset': j}
        data = (await api.get_answer(answer_id, '/comments', arg=arg)).json()
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


async def get_question_comment(question_id: int) -> None:
    num = (await api.get_question(question_id, '/comments', arg={'limit': 1})).json().get(
        'paging', {}).get('totals', 0)
    for j in range(0, num, 20):
        arg = {'limit': 20, 'offset': j}
        data = (await api.get_question(question_id, '/comments', arg=arg)).json()
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


async def get_article_comment(article_id: int) -> None:
    num = (await api.get_article(article_id, '/comments', arg={'limit': 1})).json().get('paging',
                                                                                        {}).get(
        'totals', 0)
    for j in range(0, num, 20):
        arg = {'limit': 20, 'offset': j}
        data = (await api.get_article(article_id, '/comments', arg=arg)).json()
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


async def get_all_topic() -> None:
    topic_list = [23507285, 26640843, 27795532, 20205523, 25671250, 23560902, 21763228]
    # topic_list = [23507285]
    tasks = [asyncio.create_task(get_topic(i)) for i in topic_list]
    for task in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc='Topic'):
        await task


async def get_all_question_answer() -> None:
    question_list = [i[0] for i in db.session.query(
        distinct(zhihu_question.uid)).all()]
    tasks = [asyncio.create_task(get_question_answer(i))
             for i in question_list]
    for task in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc='Question Answer'):
        # await task
        asyncio.run(task)

async def get_all_answer_comment() -> None:
    answer_list = [i[0]
                   for i in db.session.query(distinct(zhihu_answer.uid)).all()]
    tasks = [asyncio.create_task(get_answer_comment(i)) for i in answer_list]
    for task in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc='Answer Comment'):
        # await task
        asyncio.run(task)


async def get_all_question_comment() -> None:
    question_list = [i[0] for i in db.session.query(
        distinct(zhihu_question.uid)).all()]
    tasks = [asyncio.create_task(get_question_comment(i))
             for i in question_list]
    for task in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc='Question Comment'):
        # await task
        asyncio.run(task)


async def get_all_article_comment() -> None:
    article_list = [i[0]
                    for i in db.session.query(distinct(zhihu_article.uid)).all()]
    tasks = [asyncio.create_task(get_article_comment(i)) for i in article_list]
    for task in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc='Article Comment'):
        # await task
        asyncio.run(task)


def main():
    asyncio.run(get_all_topic())
    asyncio.run(get_all_question_answer())
    asyncio.run(get_all_article_comment())
    asyncio.run(get_all_question_comment())
    asyncio.run(get_all_answer_comment())


if __name__ == '__main__':
    # save_cookies()
    # exit(0)
    load_all_cookies()
    db = Database(
        'mysql+pymysql://root:20131114@localhost:3306/zhihu?charset=utf8mb4')
    # drop all table
    # Base.metadata.drop_all(db.engine)
    db.create_all_table()

    main()
    pass
