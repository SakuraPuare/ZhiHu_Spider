import time

from utils import load_all_cookies, cookies_list

from selenium import webdriver


def main():
    driver = webdriver.Chrome()
    load_all_cookies()
    for cookies in cookies_list:
        driver.get('https://www.zhihu.com/')
        for key, value in cookies.items():
            driver.add_cookie({'name': key, 'value': value})

        time.sleep(1)
        driver.get('https://www.zhihu.com/')
        pass


if __name__ == '__main__':
    main()
