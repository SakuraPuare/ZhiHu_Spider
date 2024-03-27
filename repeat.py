from sqlalchemy import func, Table, MetaData
from database import Database, zhihu_question, zhihu_answer, zhihu_article, zhihu_topic, zhihu_user, zhihu_comment


def distinct(table):
    dump = (db.session.query(table.uid).having(func.count(table.uid) > 1)
            .group_by(table.uid).all())

    for row in dump:
        rows = db.session.query(table).filter(
            table.uid == row[0]).all()
        for i in rows[1:]:
            db.session.delete(i)
    db.session.commit()
    pass

if __name__ == '__main__':
    db = Database(
        'mysql+pymysql://root:20131114@localhost:3306/zhihu?charset=utf8mb4')
    distinct(zhihu_answer)
    distinct(zhihu_article)
    distinct(zhihu_comment)
    distinct(zhihu_question)
    distinct(zhihu_topic)
    distinct(zhihu_user)
