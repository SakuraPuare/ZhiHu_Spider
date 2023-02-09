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
