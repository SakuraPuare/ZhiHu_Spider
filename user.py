import json
from pathlib import Path

import httpx
import tqdm
from selenium import webdriver

from connection import API
from database import *

sql = SQL()
api = API()

httpx_cookies = httpx.Cookies()
cookies_path = Path('cookies.json')


def get_cookies() -> None:
    global httpx_cookies
    if cookies_path.exists():
        with open(cookies_path, 'r') as f:
            cookies = json.load(f)
    else:
        driver = webdriver.Chrome()
        driver.get('https://www.zhihu.com/signin?next=%2F')
        while True:
            if driver.current_url == 'https://www.zhihu.com/':
                break
        cookies = driver.get_cookies()
        with open(cookies_path, 'w') as f:
            json.dump(cookies, f, ensure_ascii=False)
    for cookie in cookies:
        httpx_cookies.set(cookie.get('name'), cookie.get('value'), domain=cookie.get('domain'))


data = sql.fetchall('select * from user')
bar = tqdm.tqdm(data)
with httpx.Client() as client:
    for i in bar:
        id = i[0]
        if id < 165:
            continue

        if i[1] == '0':
            continue
        url = i[5]
        resp = client.get(url, cookies=httpx_cookies).json()
        ip_location = resp.get('ip_info', '').split('IP 属地')[-1]
        answer_count = resp.get('answer_count', 0)
        question_count = resp.get('question_count', 0)
        articles_count = resp.get('articles_count', 0)
        medal = resp.get('exposed_medal', {}).get('medal_name', '')

        sql_text = f'update user set ip_location="{ip_location}", answer_count={answer_count}, question_count={question_count}, articles_count={articles_count}, medal="{medal}" where id={id};'
        sql.execute(sql_text)
