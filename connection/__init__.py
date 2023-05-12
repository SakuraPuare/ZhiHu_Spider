import httpx
from urllib.parse import urlencode


class API:
    base_url = 'https://api.zhihu.com/'
    v4_url = 'https://www.zhihu.com/api/v4/'

    def get(self, msg: str, cookies: httpx.Cookies, types: str = 'base') -> httpx.Response:
        if types == 'base':
            url = self.base_url
        elif types == 'v4':
            url = self.v4_url
        else:
            raise ValueError('types must be "base" or "v4"')
        resp = httpx.get(url + msg, cookies=cookies, follow_redirects=True)
        assert resp.status_code == 200
        return resp

    def get_topic(self, ids: int, path: str, cookies: httpx.Cookies, arg=None,
                  types: str = 'base') -> httpx.Response:
        if arg is None:
            arg = {}
        msg = f'topics/{ids}' + path + (('?' + urlencode(arg)) if urlencode(arg) else '')
        return self.get(msg, cookies, types=types)

    def get_article(self, ids: int, path: str, cookies: httpx.Cookies, arg=None, types: str = 'base') -> httpx.Response:
        if arg is None:
            arg = {}
        msg = f'articles/{ids}' + path + (('?' + urlencode(arg)) if urlencode(arg) else '')
        return self.get(msg, cookies, types=types)

    def get_answer(self, ids: int, path: str, cookies: httpx.Cookies, arg=None, types: str = 'base') -> httpx.Response:
        if arg is None:
            arg = {}
        msg = f'answers/{ids}' + path + (('?' + urlencode(arg)) if urlencode(arg) else '')
        return self.get(msg, cookies, types=types)

    def get_question(self, ids: int, path: str, cookies: httpx.Cookies, arg=None,
                     types: str = 'base') -> httpx.Response:
        if arg is None:
            arg = {}
        msg = f'questions/{ids}' + path + (('?' + urlencode(arg)) if urlencode(arg) else '')
        return self.get(msg, cookies, types=types)
