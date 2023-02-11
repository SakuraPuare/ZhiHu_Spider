from tqdm import tqdm

from database import *

sql = SQL()

data = sql.fetchall('select * from question;')
bar = tqdm(data)
for i in bar:
    id = i[0]
    uid = i[1]
    url = f'https://api.zhihu.com/questions/{uid}'
    real_url = f'https://www.zhihu.com/question/{uid}'
    sql_text = f'update question set url="{url}", real_url="{real_url}" where id={id};'
    sql.execute(sql_text)
