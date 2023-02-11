import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from database import SQL

question = ['/question/542603514', '/question/542616213', '/question/542755688', '/question/542732207',
            '/question/542726552',
            '/question/542716619', '/question/542717424', '/question/543013726', '/question/542736795',
            '/question/542717060',
            '/question/542670344', '/question/542726504', '/question/542717631', '/question/542726437',
            '/question/543070263',
            '/question/542726055', '/question/542745625', '/question/542726753', '/question/542766464',
            '/question/542567233',
            '/question/542722627', '/question/543014787', '/question/542725263', '/question/542673247',
            '/question/542778378',
            '/question/542593077', '/question/542686788', '/question/542724131', '/question/542731691',
            '/question/542814216',
            '/question/542593286', '/question/542666578', '/question/542728581', '/question/542736809',
            '/question/542669504',
            '/question/542906078', '/question/542682113', '/question/542953341', '/question/542570481',
            '/question/542678997',
            '/question/543000185', '/question/542716925', '/question/542666140', '/question/542716692',
            '/question/542739597',
            '/question/542717300', '/question/542683050', '/question/542872582', '/question/542615821',
            '/question/543384493',
            '/question/542856526', '/question/542660777', '/question/542718925', '/question/542575823',
            '/question/542827767',
            '/question/542634683', '/question/542716721', '/question/542671223', '/question/542682742',
            '/question/543105863',
            '/question/542740289', '/question/542506546', '/question/542729668', '/question/542659596',
            '/question/544512554',
            '/question/542727250', '/question/543473603', '/question/542726432', '/question/543070797',
            '/question/542730395',
            '/question/542670761', '/question/19581624', '/question/542861353', '/question/542711503',
            '/question/542717284',
            '/question/543042801', '/question/543079565', '/question/542728710', '/question/542673184']

question = [i.split('/')[-1] for i in question]
driver = webdriver.Chrome()

# 登录
# driver.get('https://www.zhihu.com/signin?next=%2F')
# with open('cookies.json', 'r') as f:
#     cookies = json.load(f)
#     for cookie in cookies:
#         driver.add_cookie(cookie)
sql = SQL()

for i in question:
    url = f'https://www.zhihu.com/question/{i}'
    driver.get(url)
    uid = i
    author_id = ''
    title = driver.find_element(By.CSS_SELECTOR, '.QuestionPage > meta[itemprop=name]').get_attribute('content')
    created_time = driver.find_element(By.CSS_SELECTOR, '.QuestionPage > meta[itemprop=dateCreated]').get_attribute(
        'content')
    updated_time = driver.find_element(By.CSS_SELECTOR, '.QuestionPage > meta[itemprop=dateModified]').get_attribute(
        'content')

    created_time = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(created_time, '%Y-%m-%dT%H:%M:%S.%fZ'))
    updated_time = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(updated_time, '%Y-%m-%dT%H:%M:%S.%fZ'))
    question_type = ''

    sql_insert = f"""insert into question (uid, author_id, title, created_time, updated_time, question_type) 
    values ('{uid}', '{author_id}', '{title}', '{created_time}', '{updated_time}', '{question_type}');"""
    sql.execute(sql_insert)
    pass
