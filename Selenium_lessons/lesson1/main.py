from selenium import webdriver
import time
from random import choice
from fake_useragent import UserAgent


"""Подмена User-Agent"""

# URL = 'https://www.instagram.com'
URL = 'https://www.whatismybrowser.com/detect/what-is-my-user-agent'

WEBDRIVER_PATH_CHROME = 'C:\\Users\\lexas\\PycharmProjects\\Training_projects\\' \
                 'Parsers_training_project\\Selenium_lessons\\chromedriver.exe'

WEBDRIVER_PATH_FIREFOX = 'C:\\Users\\lexas\\PycharmProjects\\Training_projects\\' \
                         'Parsers_training_project\\Selenium_lessons\\geckodriver.exe'

# Можем создать список user-agent и выдергивать рандомно или в цикле от туда значения в опции

USER_AGENTS_LIST = [
    'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SCH-I535 Build/KOT49H) AppleWebKit/534.30 '
    '(KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',

    'Opera/9.80 (J2ME/MIDP; Opera Mini/5.1.21214/28.2725; U; ru) Presto/2.8.119 Version/11.10',

    'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 '
    '(KHTML, like Gecko) FxiOS/7.5b3349 Mobile/14F89 Safari/603.2.4',

    'Mozilla/5.0 (BB10; Kbd) AppleWebKit/537.35+ (KHTML, like Gecko) Version/10.3.3.2205 Mobile Safari/537.35+'

    ]
# или можем воспользоваться библиотекой fake_useragent
USERAGENT = UserAgent()


def get_html_by_chrome(url):
    """Автоматизация браузера Chrome, c подменой user-agent"""

    options = webdriver.ChromeOptions()
    # options.add_argument('user-agent=EbaniyNasos')
    # options.add_argument(f'user-agent={choice(USER_AGENTS_LIST)}')
    options.add_argument(f'user-agent={USERAGENT.random}')
    driver = webdriver.Chrome(executable_path=WEBDRIVER_PATH_CHROME, options=options)

    try:
        driver.get(url)
        time.sleep(5)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def get_html_by_firefox(url):
    """Автоматизация браузера FireFox, c подменой user-agent"""

    useragent = UserAgent()
    options = webdriver.FirefoxOptions()

    options.set_preference('general.useragent.override', useragent.random)

    driver = webdriver.Firefox(executable_path=WEBDRIVER_PATH_FIREFOX, options=options)

    try:
        driver.get(url)
        time.sleep(5)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def main():
    # get_html_by_chrome(URL)
    get_html_by_firefox(URL)


if __name__ == '__main__':
    main()


