import json
import pathlib
import random

import httpx
from tqdm import tqdm
from selenium import webdriver

cookies_list = []
cookies_path = pathlib.Path('./cookies/')
cookies_path.mkdir(exist_ok=True)


idx = 0

def remove_cookies(cookies: httpx.Cookies) -> None:
    global cookies_list, idx
    # cookies_list.remove(cookies)
    tqdm.write(f'Remove cookies {cookies.file_name}')
    idx %= len(cookies_list)


def load_all_cookies() -> None:
    global cookies_list
    for cookies in pathlib.Path(cookies_path).glob('*.json'):
        with open(cookies, 'r', encoding='u8') as f:
            s = json.load(f)
            httpx_cookies = httpx.Cookies()
            for key in s:
                httpx_cookies.set(key['name'], key['value'], domain=key['domain'], path=key['path'])
            httpx_cookies.file_name = cookies.stem
            cookies_list.append(httpx_cookies)


def save_cookies() -> None:
    def auto_increment() -> int:
        cookies = list(pathlib.Path(cookies_path).glob('*.json'))
        if not cookies:
            return 1
        return max([int(i.stem) for i in cookies]) + 1

    driver = webdriver.Chrome()
    driver.get('https://www.zhihu.com/signin?next=%2F')
    while True:
        if driver.current_url == 'https://www.zhihu.com/':
            break
    cookies = driver.get_cookies()
    with open(cookies_path / f'{auto_increment()}.json', 'w') as f:
        json.dump(cookies, f, ensure_ascii=False)


def get_random_cookies() -> httpx.Cookies:
    if len(cookies_list) == 0:
        raise NotImplementedError('No cookies')
    global idx
    idx %= len(cookies_list)
    cookies = cookies_list[idx]
    idx += 1
    return cookies
