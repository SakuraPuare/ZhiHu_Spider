from database import *

sql = SQL()

table_list = [Answer, User, Comment, Question, Topic, User, Article ]

for table in table_list:
    table = table()
    sql._execute('select * from %s' % table.name)
    data = [row[:2] for row in sql.cursor.fetchall()]
    after = dict()
    remove_list = []
    for i in data:
        if after.get(i[1], None):
            remove_list.append(i[0])
        else:
            after[i[1]] = i[0]
    if remove_list:
        sql._execute('delete from %s where id in (%s)' % (table.name, ','.join([str(i) for i in remove_list])))
