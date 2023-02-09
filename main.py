import asyncio
import json
import pathlib
import time

import httpx
from selenium import webdriver

from database import SQL

cookies_path = pathlib.Path('cookies.json')

topic_id = 25850855

sql = SQL()
driver = webdriver.Chrome()


def read_cookies(path: pathlib.Path = 'cookies.json') -> dict:
    with open(cookies_path, 'r') as f:
        cookies = json.load(f)
        return cookies


def save_cookies(path: pathlib.Path = 'cookies.json') -> None:
    cookies = driver.get_cookies()
    with open(cookies_path, 'w') as f:
        json.dump(cookies, f, ensure_ascii=False)


def get_cookies() -> httpx.Cookies:
    httpx_cookies = httpx.Cookies()
    cookies = driver.get_cookies()
    for cookie in cookies:
        httpx_cookies.set(cookie.get('name'), cookie.get('value'), domain=cookie.get('domain'))
    return httpx_cookies


async def get(msg: str, kwarg: Union[dict, str] = '') -> dict:
    async with httpx.AsyncClient(cookies=get_cookies()) as client:
        url = f'https://www.zhihu.com/api/v4/' + msg + kwarg
        request = await client.get(url=url, follow_redirects=True, **kwargs)
        assert request.status_code == 200
        return request.json()


async def get_topic(ids: int, types: str = '') -> dict:
    msg = f'topics/{ids}' + types
    return await get(msg)


async def main():
    # response = await get_topic(topic_id)
    # sql.insert_into('topic_intro', TopicIntro, response)

    pass


if __name__ == '__main__':

    driver.get('https://www.zhihu.com/signin')
    # 加载cookies
    if cookies_path.exists():
        cookies = read_cookies()
        for cookie in cookies:
            driver.add_cookie(cookie)
    else:

        driver.refresh()
        driver.implicitly_wait(10)

        while driver.current_url != 'https://www.zhihu.com/':
            time.sleep(0.5)

        save_cookies()

    asyncio.run(main())
