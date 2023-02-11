import html
import time
from typing import Union, Any, Type

import pymysql
from bs4 import BeautifulSoup

from .config import config


class Tables:
    name = ''
    keys = []
    types = []
    description = ''

    def __init__(self) -> None:
        pass

    @property
    def key(self) -> str:
        return ', '.join(self.keys)

    @property
    def type(self) -> str:
        return ', \n'.join([' '.join(i) for i in self.types])

    @staticmethod
    def _fmt_time(t: str) -> str:
        t = time.localtime(int(t))
        return time.strftime('%Y-%m-%d %H:%M:%S', t)

    @staticmethod
    def _fmt_bool(b: bool) -> int:
        return 1 if b else 0

    def tolist(self, data: Union[dict, list[dict]]) -> list:
        if isinstance(data, dict):
            data = [data]
        result = set()
        for i in data:
            result.add(tuple())
        return list(result)

    @staticmethod
    def str(data: Union[dict, list[dict]]) -> str:
        return f"""( {', '.join(f'"{i}"' for i in data[0])} )""" if len(data) == 1 else ', \n'.join(
            [f"""( {', '.join(f'"{j}"' for j in i)} )""" for i in data])

    def value(self, data: Union[dict, list[dict]]) -> str:
        data = self.tolist(data)
        return self.str(data)


class Topic(Tables):
    name = 'topic'
    keys = ['uid', 'name', 'url', 'created', 'updated', 'introduction', 'followers_count', 'question_count',
            'avatar_url', 'best_answers_count']
    types = [
        ('id', 'int', 'auto_increment', 'primary', 'key'),
        ('uid', 'varchar(64)', "comment '话题id'"),
        ('name', 'varchar(256)', "comment '话题名称'"),
        ('url', 'varchar(256)', "comment '话题url'"),
        ('created', 'timestamp', "comment '创建时间'"),
        ('updated', 'timestamp', "comment '更新时间'"),
        ('introduction', 'text', "comment '话题介绍'"),
        ('followers_count', 'int', "comment '关注数量'"),
        ('question_count', 'int', "comment '问题数量'"),
        ('avatar_url', 'varchar(256)', "comment '话题头像'"),
        ('best_answers_count', 'int', "comment '最佳回答数量'")
    ]

    description = '话题信息'

    def __init__(self) -> None:
        super().__init__()

    def tolist(self, data: Union[dict, list[dict]]) -> list:
        if isinstance(data, dict):
            data = [data]
        result = set()
        for i in data:
            uid = i.get('id', '')
            name = i.get('name', '')
            url = i.get('url', '')
            created = self._fmt_time(i.get('created', ''))
            updated = self._fmt_time(i.get('updated', ''))
            introduction = html.escape(i.get('introduction', ''))
            followers_count = i.get('followers_count', -1)
            questions_count = i.get('questions_count', -1)
            avatar_url = i.get('avatar_url', '')
            best_answers_count = i.get('best_answers_count', -1)
            result.add((uid, name, url, created, updated, introduction, followers_count, questions_count, avatar_url,
                        best_answers_count))
        return list(result)


class User(Tables):
    name = 'user'
    keys = ['uid', 'name', 'gender', 'user_type', 'url', 'badge']
    types = [
        ('id', 'bigint', 'auto_increment', 'primary key'),
        ('uid', 'varchar(64)', "comment '用户id'"),
        ('name', 'varchar(32)', "comment '昵称'"),
        ('gender', 'smallint', "comment '性别'"),
        ('user_type', 'varchar(32)', "comment '用户类型'"),
        ('url', 'text', "comment '用户url'"),
        ('badge', 'varchar(32)', "comment '头衔'")
    ]

    description = '用户信息'

    def __init__(self) -> None:
        super().__init__()

    def tolist(self, data: Union[dict, list[dict]]) -> list:
        if isinstance(data, dict):
            data = [data]
        result = set()
        for author in data:
            name = author.get('name', '')
            uid = author.get('id', '')
            gender = author.get('gender', -1)
            user_type = author.get('user_type', '')
            url = author.get('url', '')
            badge = ', '.join([i.get('description', '') for i in author.get('badge')]) if author.get('badge',
                                                                                                     None) else ''
            result.add((uid, name, gender, user_type, url, badge))
        return list(result)


class Answer(Tables):
    name = 'answer'
    keys = ['uid', 'question_id', 'author_id', 'created_time', 'updated_time', 'voteup_count', 'favlists_count',
            'comment_count', 'url', 'content', 'content_text', 'is_labeled']
    types = [
        ('id', 'bigint', 'auto_increment', 'primary key'),
        ('uid', 'bigint', "comment '回答uid'"),
        ('question_id', 'bigint', "comment '问题uid'"),
        ('author_id', 'varchar(64)', "comment '回答作者uid'"),
        ('created_time', 'timestamp', "comment '回答创建时间'"),
        ('updated_time', 'timestamp', "comment '修改时间'"),
        ('voteup_count', 'bigint', "comment '赞同数量'"),
        ('favlists_count', 'bigint', "comment '收藏数量'"),
        ('comment_count', 'bigint', "comment '评论数量'"),
        ('url', 'varchar(256)', "comment '回答链接'"),
        ('content', 'text', "comment '内容'"),
        ('content_text', 'text', "comment '纯文本'"),
        ('is_labeled', 'bool')
    ]

    description = '回答信息'

    def __init__(self) -> None:
        super().__init__()

    def tolist(self, data: Union[dict, list[dict]]) -> list:
        if isinstance(data, dict):
            data = [data]
        result = set()
        for answer in data:
            uid = answer.get('id', 0)
            question_id = answer.get('question').get('id', 0)
            author_id = answer.get('author').get('id', '')
            created_time = self._fmt_time(answer.get('created_time', '0'))
            updated_time = self._fmt_time(answer.get('updated_time', '0'))
            content = html.escape(answer.get('content', ''))
            content_text = BeautifulSoup(answer.get('content', ''), 'html.parser').get_text().replace('"', "'").strip()
            voteup_count = answer.get('voteup_count', -1)
            favlists_count = answer.get('favlists_count', -1)
            comment_count = answer.get('comment_count', -1)
            url = answer.get('url', '')
            is_labeled = self._fmt_bool(answer.get('is_labeled', False))
            result.add(
                (uid, question_id, author_id, created_time, updated_time, voteup_count, favlists_count, comment_count,
                 url, content, content_text, is_labeled))
        return list(result)


class Article(Tables):
    name = 'article'
    keys = ['uid', 'author_id', 'url', 'created', 'updated', 'voteup_count', 'comment_count', 'favlists_count', 'title',
            'content', 'content_text', 'is_labeled']
    types = [
        ('id', 'bigint', 'auto_increment', 'primary key'),
        ('uid', 'bigint', "comment '文章id'"),
        ('author_id', 'varchar(64)', "comment '作者id'"),
        ('url', 'varchar(256)', "comment '文章链接'"),
        ('created', 'timestamp', "comment '创建时间'"),
        ('updated', 'timestamp', "comment '更新时间'"),
        ('voteup_count', 'bigint', "comment '赞同数量'"),
        ('comment_count', 'bigint', "comment '评论数量'"),
        ('favlists_count', 'bigint', "comment '收藏数量'"),
        ('title', 'varchar(256)', "comment '文章标题'"),
        ('content', 'text', "comment '文章正文'"),
        ('content_text', 'text', "comment '纯文本'"),
        ('is_labeled', 'bool',),
    ]

    description = '文章信息'

    def __init__(self) -> None:
        super().__init__()

    def tolist(self, data: Union[dict, list[dict]]) -> list[tuple]:
        if isinstance(data, dict):
            data = [data]
        result = set()
        for article in data:
            uid = article.get('id')
            updated = self._fmt_time(article.get('updated', '0'))
            is_labeled = self._fmt_bool(article.get('is_labeled'))
            voteup_count = article.get('voteup_count')
            author_id = article.get('author').get('id')
            url = article.get('url')
            created = self._fmt_time(article.get('created', '0'))
            comment_count = article.get('comment_count')
            title = article.get('title')
            content = html.escape(article.get('content'))
            content_text = BeautifulSoup(article.get('content', ''), 'html.parser').get_text().replace('"', "'").strip()
            favlists_count = article.get('favlists_count')
            result.add(
                (uid, author_id, url, created, updated, voteup_count, comment_count, favlists_count, title, content,
                 content_text, is_labeled))
        return list(result)


class Question(Tables):
    name = 'question'
    keys = ['uid', 'author_id', 'title', 'created_time', 'updated_time', 'question_type']
    types = [
        ('id', 'bigint', 'auto_increment', 'primary key'),
        ('uid', 'bigint', "comment '问题id'"),
        ('author_id', 'varchar(64)', "comment '提问者id'"),
        ('title', 'varchar(512)', "comment '问题标题'"),
        ('created_time', 'timestamp', "comment '创建时间'"),
        ('updated_time', 'timestamp', "comment '更新时间'"),
        ('question_type', 'varchar(32)', "comment '问题类型'")
    ]

    description = '问题信息'

    def __init__(self) -> None:
        super().__init__()

    def tolist(self, data: Union[dict, list[dict]]) -> list:
        if isinstance(data, dict):
            data = [data]
        result = set()
        for question in data:
            uid = question.get('id', 0)
            author_id = question.get('author', {}).get('id', '')
            title = question.get('title')
            created_time = self._fmt_time(question.get('created', '0'))
            updated_time = self._fmt_time(question.get('updated_time', '0'))
            question_type = question.get('type', '')
            result.add((uid, author_id, title, created_time, updated_time, question_type))
        return list(result)


class Comment(Tables):
    name = 'comment'
    keys = ['uid', 'author_id', 'content', 'content_text', 'created_time', 'vote_count', 'reply_to_author', 'url',
            'address_text', 'from_where']
    types = [
        ('id', 'bigint', 'auto_increment', 'primary key'),
        ('uid', 'bigint', "comment '评论id'"),
        ('author_id', 'varchar(64)', "comment '评论者id'"),
        ('content', 'text', "comment '评论内容'"),
        ('content_text', 'text', "comment '纯文本'"),
        ('created_time', 'timestamp', "comment '创建时间'"),
        ('vote_count', 'bigint', "comment '赞同数量'"),
        ('reply_to_author', 'varchar(64)', "comment '回复者id'"),
        ('url', 'varchar(256)', "comment '评论url'"),
        ('address_text', 'varchar(16)', "comment '评论地址'"),
        ('from_where', 'varchar(32)', "comment '来自'")
    ]

    def __init__(self) -> None:
        super().__init__()

    def tolist(self, data: Union[list[dict], dict]) -> list:
        if isinstance(data, dict):
            data = [data]
        result = set()
        for comment in data:
            uid = comment.get('id', 0)
            author_id = comment.get('author', {}).get('member', {}).get('id', '')
            content = html.escape(comment.get('content'))
            content_text = BeautifulSoup(comment.get('content', ''), 'html.parser').get_text().replace('"', "'").strip()
            created_time = self._fmt_time(comment.get('created_time', '0'))
            vote_count = comment.get('vote_count')
            reply_to_author = comment.get('reply_to_author', {}).get('member', {}).get('id', '')
            url = comment.get('url')
            address_text = comment.get('address_text', 'IP 属地').split('IP 属地')[-1]
            from_where = 'article'
            result.add(
                (uid, author_id, content, content_text, created_time, vote_count, reply_to_author, url, address_text,
                 from_where))
        return list(result)


class SQL:
    def __init__(self, host: str = config.host, user: str = config.username, password: str = config.password,
                 dbname: str = config.dbname, charset: str = 'utf8mb4') -> None:
        self.host = host
        self.user = user
        self.password = password
        self.dbname = dbname

        self.db = pymysql.connect(host=self.host, user=self.user, password=self.password, charset=charset)
        self.cursor = self.db.cursor()
        self.init()
        self.execute("USE `{}`;".format(self.dbname))

    def fetchall(self, sql: str) -> tuple[tuple[Any, ...], ...]:
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def execute(self, sql: str, ) -> Union[tuple, None]:
        self.cursor.execute(sql)
        try:
            self.db.commit()
            result = self.cursor.fetchone()
            return result
        except Exception as e:
            self.db.rollback()
            print(e)
            return None

    def init(self) -> None:
        self.execute(
            "CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;".format(
                config.dbname))
        self.execute("USE `{}`;".format(config.dbname))

        # 初始化数据库
        init_list = [Topic(), User(), Answer(), Article(), Question(), Comment()]
        for i in init_list:
            self.execute(
                f"create table if not exists `{i.name}` ({i.type}) comment '{i.description}';")

    def select(self, table: str, key: Union[list, tuple], value: Union[list, tuple]) -> Union[tuple, None]:
        where = ' and '.join([f"""{key[i]} = "{value[i]}" """ for i in range(len(key))])
        sql = f"""select * from `{table}` where {where};"""
        return self.execute(sql)

    def insert_into(self, table: str, types: Type[Tables], data: Any) -> None:
        types = types()
        key = types.keys
        value = types.tolist(data)

        for i in value:
            if self.select(table, key[:2], i[:2]):
                continue
            else:
                sql = f"""insert into `{table}` ({types.key}) values {types.str([i])};"""
                self.execute(sql)
        # insert = []
        # for i in value:
        #     if self.select(table, key, i):
        #         continue
        #     else:
        #         insert.append(i)
        # if insert:
        #     sql = f"""insert into `{table}` ({types.key}) values {types.str(insert)};"""
        #     return self._execute(sql)
        # else:
        #     return None

    def create_table(self, table: str, types: Type[Tables]) -> None:
        types = types()
        sql = f"""create table if not exists `{table}` ({types.type}) comment '{types.description}';"""
        self.execute(sql)
