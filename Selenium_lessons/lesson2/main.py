# from selenium import webdriver
from seleniumwire import webdriver # понадобится нам для расширения работы webdriver
import time
from random import choice
from fake_useragent import UserAgent
from proxy_auth_data import LOGIN, PASSWORD


"""Подключаем прокси"""

# URL = 'https://www.instagram.com'
URL = 'https://www.whatismybrowser.com/detect/what-is-my-user-agent'

WEBDRIVER_PATH_CHROME = 'C:\\Users\\lexas\\PycharmProjects\\Training_projects\\' \
                 'Parsers_training_project\\Selenium_lessons\\chromedriver.exe'

WEBDRIVER_PATH_FIREFOX = 'C:\\Users\\lexas\\PycharmProjects\\Training_projects\\' \
                         'Parsers_training_project\\Selenium_lessons\\geckodriver.exe'


USERAGENT = UserAgent()


def get_html_by_chrome(url, useragent):
    """Автоматизация браузера Chrome, c подменой user-agent и прокси c привязкой и без привязки к ip"""

    options = webdriver.ChromeOptions()

    options.add_argument(f'user-agent={useragent.random}')

    # подключаем прокси с привязкой ip
    options.add_argument('--proxy-server=138.128.91.65:8000')

    # более анонимно, настройка для прокси без привязки к ip
    proxy_options = {
        'proxy': {
            'https': f'http://{LOGIN}:{PASSWORD}@138.128.91.65:8000'
        }
    }
    #  для прокси без привязки к ip используем webdriver из seleniumwire и спец опция proxy_options
    #  если нам хватит прокси с привязкой, то можем использовать обычный options
    driver = webdriver.Chrome(executable_path=WEBDRIVER_PATH_CHROME, seleniumwire_options=proxy_options)

    try:
        driver.get(url)
        time.sleep(5)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def get_html_by_firefox(url):
    """Автоматизация браузера FireFox, c подменой user-agent и прокси c привязкой и без привязки к ip"""

    useragent = UserAgent()
    options = webdriver.FirefoxOptions()

    options.set_preference('general.useragent.override', useragent.random)
    # подключаем прокси с привязкой ip, это несколько сложнее чем с Chrome
    proxy = '138.128.91.65:8000'
    firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
    firefox_capabilities['marionette'] = True
    firefox_capabilities['proxy'] = {
        'proxyType': 'MANUAL',
        'httpProxy': proxy,
        'ftpProxy': proxy,
        'sslProxy': proxy
    }

    # более анонимно, настройка для прокси без привязки к ip
    proxy_options = {
        'proxy': {
            'https': f'http://{LOGIN}:{PASSWORD}@138.128.91.65:8000'
        }
    }

    #  для прокси без привязки к ip используем webdriver из seleniumwire и спец опция proxy_options
    #  если нам хватит прокси с привязкой, то можем использовать обычный selenium и параметры options и proxy
    driver = webdriver.Firefox(executable_path=WEBDRIVER_PATH_FIREFOX, proxy_options=proxy_options)

    try:
        driver.get(url)
        time.sleep(5)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def main():
    get_html_by_chrome(URL, USERAGENT)
    # get_html_by_firefox(URL)


if __name__ == '__main__':
    main()