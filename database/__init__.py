import datetime
import html
from typing import Union, Iterable

from bs4 import BeautifulSoup
from sqlalchemy import create_engine, String, Column, Float, Integer, DateTime, Boolean, BigInteger
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


class Database:
    def __init__(self, db_url: str) -> None:
        self.engine = create_engine(db_url, echo=True)
        self.session = sessionmaker(bind=self.engine)()

    def init(self) -> None:
        self.create_all_table()

    def create_all_table(self) -> None:
        Base.metadata.create_all(self.engine)

    def inserts(self, obj: Union[Iterable[Base], Base]) -> None:
        if isinstance(obj, list):
            self.session.add_all(obj)
        else:
            self.session.add(obj)
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def close(self) -> None:
        self.session.close()
        self.engine.dispose()



class zhihu_topic(Base):
    __tablename__ = 'zhihu_topic'
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String(255), comment='话题id')
    name = Column(String(255), comment='话题名')
    url = Column(String(255), comment='话题链接')
    created = Column(DateTime, comment='创建时间')
    updated = Column(DateTime, comment='更新时间')
    introduction = Column(LONGTEXT, comment='话题简介')
    followers = Column(BigInteger, comment='关注人数')
    questions = Column(BigInteger, comment='问题数')
    avatar_url = Column(String(255), comment='话题头像链接')
    best_answers = Column(Integer, comment='最佳回答数')

    def __repr__(self):
        return f'<zhihu_topic(uid={self.uid}, name={self.name}, url={self.url}, created={self.created})>'

    @classmethod
    def load(cls, data: dict):
        uid = data.get('id', -1)
        name = data.get('name', '')
        url = data.get('url', '')
        created = datetime.datetime.fromtimestamp(data.get('created', 0))
        updated = datetime.datetime.fromtimestamp(data.get('updated', 0))
        introduction = html.escape(data.get('introduction', ''))
        followers = data.get('followers_count', 0)
        questions = data.get('questions_count', 0)
        avatar_url = data.get('avatar_url', '')
        best_answers = data.get('best_answers_count', 0)
        return cls(uid=uid, name=name, url=url, created=created, updated=updated, introduction=introduction,
                   followers=followers, questions=questions, avatar_url=avatar_url, best_answers=best_answers)


class zhihu_user(Base):
    __tablename__ = 'zhihu_user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String(255), comment='用户id')
    name = Column(String(255), comment='用户名')
    gender = Column(Integer, comment='性别')
    user_type = Column(String(255), comment='用户类型')
    url = Column(LONGTEXT, comment='用户链接')
    badge = Column(String(255), comment='用户标签')

    def __repr__(self):
        return f'<zhihu_user(uid={self.uid}, name={self.name})>'

    @classmethod
    def load(cls, data: dict):
        uid = data.get('id', -1)
        name = data.get('name', '')
        gender = data.get('gender', -1)
        user_type = data.get('user_type', '')
        url = data.get('url', '')
        badge = ', '.join([i.get('description', '') for i in data.get('badge')]) if data.get('badge', None) else ''
        return cls(uid=uid, name=name, gender=gender, user_type=user_type, url=url, badge=badge)


class zhihu_answer(Base):
    __tablename__ = 'zhihu_answer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String(255), comment='回答id')
    question_id = Column(String(255), comment='问题id')
    author_id = Column(String(255), comment='作者id')
    created = Column(DateTime, comment='创建时间')
    updated = Column(DateTime, comment='更新时间')
    voteup_count = Column(BigInteger, comment='点赞数')
    comment_count = Column(BigInteger, comment='评论数')
    favlists_count = Column(BigInteger, comment='收藏数')
    url = Column(String(255), comment='回答链接')
    content = Column(LONGTEXT, comment='回答内容')
    is_label = Column(Boolean, comment='是否标注')

    def __repr__(self):
        return f'<zhihu_answer(uid={self.uid}, question_id={self.question_id}, author_id={self.author_id})>'

    @classmethod
    def load(cls, data: dict):
        uid = data.get('id', -1)
        question_id = data.get('question', {}).get('id', -1)
        author_id = data.get('author', {}).get('id', -1)
        created = datetime.datetime.fromtimestamp(data.get('created_time', 0))
        updated = datetime.datetime.fromtimestamp(data.get('updated_time', 0))
        voteup_count = data.get('voteup_count', 0)
        comment_count = data.get('comment_count', 0)
        favlists_count = data.get('favlists_count', 0)
        url = data.get('url', '')
        content = BeautifulSoup(data.get('content', ''), 'html.parser').get_text().replace('"', "'").strip()
        is_label = data.get('is_label', False)
        return cls(uid=uid, question_id=question_id, author_id=author_id, created=created, updated=updated,
                   voteup_count=voteup_count, comment_count=comment_count, favlists_count=favlists_count, url=url,
                   content=content, is_label=is_label)


class zhihu_article(Base):
    __tablename__ = 'zhihu_article'
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String(255), comment='文章id')
    author_id = Column(String(255), comment='作者id')
    url = Column(String(255), comment='文章链接')
    title = Column(String(255), comment='文章标题')
    created = Column(DateTime, comment='创建时间')
    updated = Column(DateTime, comment='更新时间')
    voteup_count = Column(BigInteger, comment='点赞数')
    comment_count = Column(BigInteger, comment='评论数')
    favlists_count = Column(BigInteger, comment='收藏数')
    content = Column(LONGTEXT, comment='文章内容')
    is_label = Column(Boolean, comment='是否标注')

    def __repr__(self):
        return f'<zhihu_article(uid={self.uid}, author_id={self.author_id}, title={self.title})>'

    @classmethod
    def load(cls, data: dict):
        uid = data.get('id', -1)
        author_id = data.get('author', {}).get('id', -1)
        url = data.get('url', '')
        title = data.get('title', '')
        created = datetime.datetime.fromtimestamp(data.get('created', 0))
        updated = datetime.datetime.fromtimestamp(data.get('updated', 0))
        voteup_count = data.get('voteup_count', 0)
        comment_count = data.get('comment_count', 0)
        favlists_count = data.get('favlists_count', 0)
        content = BeautifulSoup(data.get('content', ''), 'html.parser').get_text().replace('"', "'").strip()
        is_label = data.get('is_label', False)

        return cls(uid=uid, author_id=author_id, url=url, title=title, created=created, updated=updated,
                   voteup_count=voteup_count, comment_count=comment_count, favlists_count=favlists_count,
                   content=content, is_label=is_label)


class zhihu_question(Base):
    __tablename__ = 'zhihu_question'
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String(255), comment='问题id')
    author_id = Column(String(255), comment='作者id')
    title = Column(String(255), comment='问题标题')
    created = Column(DateTime, comment='创建时间')
    updated = Column(DateTime, comment='更新时间')
    question_type = Column(String(255), comment='问题类型')

    def __repr__(self):
        return f'<zhihu_question(uid={self.uid}, author_id={self.author_id}, title={self.title})>'

    @classmethod
    def load(cls, data: dict):
        uid = data.get('id', -1)
        author_id = data.get('author', {}).get('id', -1)
        title = data.get('title', '')
        created = datetime.datetime.fromtimestamp(data.get('created_time', 0))
        updated = datetime.datetime.fromtimestamp(data.get('updated_time', 0))
        question_type = data.get('question_type', '')
        return cls(uid=uid, author_id=author_id, title=title, created=created, updated=updated,
                   question_type=question_type)


class zhihu_comment(Base):
    __tablename__ = 'zhihu_comment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String(255), comment='评论id')
    author_id = Column(String(255), comment='作者id')
    created = Column(DateTime, comment='创建时间')
    content = Column(LONGTEXT, comment='评论内容')
    vote_count = Column(BigInteger, comment='点赞数')
    reply_to_author_id = Column(String(255), comment='回复对象id')
    url = Column(String(255), comment='评论链接')
    address = Column(String(255), comment='评论地址')
    from_where = Column(String(255), comment='评论来源')

    def __repr__(self):
        return f'<zhihu_comment(uid={self.uid}, author_id={self.author_id}, content={self.content})>'

    @classmethod
    def load(cls, data: dict):
        uid = data.get('id', -1)
        author_id = data.get('author', {}).get('member', {}).get('id', -1)
        created = datetime.datetime.fromtimestamp(data.get('created_time', 0))
        content = BeautifulSoup(data.get('content', ''), 'html.parser').get_text().replace('"', "'").strip()
        vote_count = data.get('vote_count', 0)
        reply_to_author_id = data.get('reply_to_author', {}).get('member', {}).get('id', -1)
        url = data.get('url', '')
        address = data.get('address_text', '')
        from_where = data.get('from_where', '')
        return cls(uid=uid, author_id=author_id, created=created, content=content, vote_count=vote_count,
                   reply_to_author_id=reply_to_author_id, url=url, address=address, from_where=from_where)


if __name__ == '__main__':
    db = Database('mysql+pymysql://root:20131114@localhost:3306/env?charset=utf8mb4')
    db.create_all_table()
