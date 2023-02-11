from database import *

sql = SQL()

table_list = [Answer, User, Comment, Article, Question, ]

for table in table_list:
    table = table()
    data = sql.fetchall('select * from %s' % table.name)[:2]
    after = dict()
    remove_list = []
    for i in data:
        if after.get(i[1], None):
            remove_list.append(i[0])
        else:
            after[i[1]] = i[0]
    if remove_list:
        sql.execute('delete from %s where id in (%s)' % (table.name, ','.join([str(i) for i in remove_list])))
