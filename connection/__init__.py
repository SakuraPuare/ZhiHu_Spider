import asyncio
import time
from urllib.parse import urlencode

import httpx
from tqdm import tqdm

from utils import get_random_cookies, remove_cookies

limit = asyncio.Semaphore(5)


class API:
    base_url = 'https://api.zhihu.com/'
    v4_url = 'https://www.zhihu.com/api/v4/'
    v5_url = 'https://www.zhihu.com/api/v5/'

    async def get(self, msg: str, types: str = 'base') -> httpx.Response:
        if types == 'base':
            url = self.base_url
        elif types == 'v4':
            url = self.v4_url
        elif types == 'v5':
            url = self.v5_url
        else:
            raise ValueError('types must be "base", "v4" or "v5"')
        try:
            cookies = get_random_cookies()
            async with limit:
                async with httpx.AsyncClient(follow_redirects=True, cookies=cookies, timeout=3) as client:
                    resp = await client.get(url + msg)
                    await asyncio.sleep(0.3)
            if resp.status_code == 403:
                remove_cookies(cookies)
                raise ConnectionRefusedError
            assert resp.status_code == 200
        except ConnectionRefusedError:
            # 输出状态码
            tqdm.write(f'\tError: {resp.status_code} {url + msg}')
            return await self.get(msg, types)
        except httpx.ConnectTimeout:
            return await self.get(msg, types)
        except Exception as e:
            # 输出错误类型
            tqdm.write(f'\tError: {type(e)} {url + msg}')
            return await self.get(msg, types)
        return resp

    async def get_topic(self, ids: int, path: str, arg=None,
                        types: str = 'base') -> httpx.Response:
        if arg is None:
            arg = {}
        msg = f'topics/{ids}' + path + \
              (('?' + urlencode(arg)) if urlencode(arg) else '')
        return await self.get(msg, types=types)

    async def get_article(self, ids: int, path: str, arg=None,
                          types: str = 'base') -> httpx.Response:
        if arg is None:
            arg = {}
        msg = f'articles/{ids}' + path + \
              (('?' + urlencode(arg)) if urlencode(arg) else '')
        return await self.get(msg, types=types)

    async def get_answer(self, ids: int, path: str, arg=None,
                         types: str = 'base') -> httpx.Response:
        if arg is None:
            arg = {}
        msg = f'answers/{ids}' + path + \
              (('?' + urlencode(arg)) if urlencode(arg) else '')
        return await self.get(msg, types=types)

    async def get_question(self, ids: int, path: str, arg=None,
                           types: str = 'base') -> httpx.Response:
        if arg is None:
            arg = {}
        msg = f'questions/{ids}' + path + \
              (('?' + urlencode(arg)) if urlencode(arg) else '')
        return await self.get(msg, types=types)
