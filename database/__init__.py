import html
from typing import Union, Any, Type

import pymysql

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
    def value(self, data: Any, with_bracket: bool = True) -> str:
        return '()'
        pass


class TopicIntro(Tables):
    name = 'topic_intro'
    keys = ['name', 'introduction', 'question_count', 'follow_count', 'topic_id', 'uid', 'best_answers_count',
            'avatar_url']
    types = [
        ('id', 'int', 'auto_increment', 'PRIMARY KEY'),
        ('name', 'varchar(64)', "comment '话题标题'"),
        ('introduction', 'text', "comment '简介'"),
        ('question_count', 'int', "comment '问题数量'"),
        ('follow_count', 'int', "comment '关注数量'"),
        ('topic_id', 'bigint', "comment '话题id'"),
        ('uid', 'int', "comment '话题id'"),
        ('best_answers_count', 'int'),
        ('avatar_url', 'varchar(128)')
    ]

    description = '话题简介'

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def value(data: Union[dict, list], with_bracket: bool = True, **kwargs) -> str:
        if isinstance(data, dict):
            data = [data]
        result = []
        for i in data:
            name = i.get('name', '')
            introduction = html.escape(i.get('introduction', ''))
            question_count = i.get('question_count', 0)
            follow_count = i.get('follow_count', 0)
            topic_id = i.get('topic_id', 0)
            uid = i.get('id', 0)
            best_answers_count = i.get('best_answers_count', 0)
            avatar_url = i.get('avatar_url', '')
            result.append(
                (name, introduction, question_count, follow_count, topic_id, uid, best_answers_count, avatar_url))

        return f"""( {', '.join(f'"{i}"' for i in result[0])} )""" if len(result) == 1 else ', \n'.join(
            f"""( {', '.join(f'"{i}"' for i in result[0])} )""")


class User(Tables):
    name = 'user'
    keys = ['name', 'uid', 'gender', 'user_type', 'url', 'badge']
    types = [
        ('id', 'int', 'auto_increment', 'primary key'),
        ('name', 'varchar(32)', "comment '昵称'"),
        ('uid', 'varchar(64)', "comment '用户id'"),
        ('gender', 'smallint', "comment '性别'"),
        ('user_type', 'varchar(32)', "comment '用户类型'"),
        ('url', 'text', "comment '用户url'"),
        ('badge', 'varchar(32)', "comment '头衔'")
    ]

    description = '用户信息'

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def value(data: Union[dict, list], with_bracket: bool = True, **kwargs) -> str:
        if isinstance(data, dict):
            data = [data]
        result = []
        for i in data:
            author = i.get('author', {})
            name = author.get('name', '')
            uid = author.get('id', '')
            gender = author.get('gender', -1)
            user_type = author.get('user_type', '')
            url = author.get('url', '')
            badge = author.get('badge_v2', '').get('title', '')
            result.append((name, uid, gender, user_type, url, badge))

        return f"""( {', '.join(f'"{i}"' for i in result[0])} )""" if len(result) == 1 else ', \n'.join(
            f"""( {', '.join(f'"{i}"' for i in result[0])} )""")


class Answer(Tables):
    name = 'answer'
    keys = ['uid', 'question_id', 'author_id', 'created_time', 'updated_time', 'content', 'voteup_count',
            'favlists_count', 'comment_count', 'url', 'is_labeled']
    types = [
        ('id', 'int', 'auto_increment', 'primary key'),
        ('uid', 'int', "comment 回答uid'"),
        ('question_id', 'int', "comment '问题uid'"),
        ('author_id', 'varchar(64)', "comment 回答作者uid'"),
        ('created_time', 'timestamp', "comment 回答创建时间'"),
        ('updated_time', 'timestamp', "comment 修改时间'"),
        ('content', 'text', "comment 内容'"),
        ('voteup_count', 'int', "comment 赞同数量'"),
        ('favlists_count', 'int', "comment 收藏数量'"),
        ('comment_count', 'int', "comment 评论数量'"),
        ('url', 'varchar(256)', "comment 回答链接'"),
        ('is_labeled', 'bool')
    ]

    description = '回答信息'

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def value(data: Union[dict, list], with_bracket: bool = True, **kwargs) -> str:
        pass

class SQL:
    def __init__(self, host: str = config.host, user: str = config.username, password: str = config.password,
                 dbname: str = config.dbname, charset: str = 'utf8mb4') -> None:
        self.host = host
        self.user = user
        self.password = password
        self.dbname = dbname

        self.db = pymysql.connect(host=self.host, user=self.user, password=self.password, charset=charset)
        self.cursor = self.db.cursor()
        try:
            self._execute("USE `{}`;".format(self.dbname))
        except pymysql.OperationalError as e:
            if e.args[0] == 1049:
                self.init()

    def _execute(self, sql: str) -> Union[tuple, None]:
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
        self._execute(
            "CREATE DATABASE `{}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;".format(config.dbname))
        self._execute("USE `{}`;".format(config.dbname))

        # 初始化数据库
        init_list = [TopicIntro()]
        for i in init_list:
            self._execute(
                f"create table if not exists `{i.name}` ({i.type}) comment '{i.description}';")

    def insert_into(self, table: str, types: Type[Tables], data: Any) -> Union[tuple, None]:
        types = types()
        key = types.key
        data = types.value(data)
        sql = f"""insert into `{table}` ({key}) values {data};"""
        return self._execute(sql)


if __name__ == '__main__':
    sql = SQL()
    resp = sql._execute("select * from information_schema.SCHEMATA where SCHEMA_NAME = 'test';")
    pass
