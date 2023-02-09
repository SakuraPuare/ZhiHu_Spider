import asyncio
import json
import pathlib
import time
from selenium import webdriver
cookies_path = pathlib.Path('cookies.json')
driver = webdriver.Chrome()
def read_cookies(path: pathlib.Path = 'cookies.json') -> dict:
    with open(cookies_path, 'r') as f:
        cookies = json.load(f)
        return cookies


def save_cookies(path: pathlib.Path = 'cookies.json') -> None:
    cookies = driver.get_cookies()
    with open(cookies_path, 'w') as f:
        json.dump(cookies, f, ensure_ascii=False)
async def main():
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
