from database import SQL

sql = SQL()

sql.execute('select * from user order by id')
data = sql.cursor.fetchall()

normal_list = []
error_list = []

for i in data:
    if len(i[1]) != 32 and i[1] != '0':
        error_list.append(i)
    else:
        normal_list.append(i)

for i in error_list:
    sql.execute(f'update user set uid = "{i[2]}", name = "{i[1]}" where id = {i[0]}')

pass
