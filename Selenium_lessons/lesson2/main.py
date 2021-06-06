from selenium import webdriver
#  from seleniumwire import webdriver
import time
from random import choice
from fake_useragent import UserAgent


"""Подключаем прокси"""

# URL = 'https://www.instagram.com'
URL = 'https://www.whatismybrowser.com/detect/what-is-my-user-agent'

WEBDRIVER_PATH_CHROME = 'C:\\Users\\lexas\\PycharmProjects\\Training_projects\\' \
                 'Parsers_training_project\\Selenium_lessons\\chromedriver.exe'

WEBDRIVER_PATH_FIREFOX = 'C:\\Users\\lexas\\PycharmProjects\\Training_projects\\' \
                         'Parsers_training_project\\Selenium_lessons\\geckodriver.exe'


USERAGENT = UserAgent()


def get_html_by_chrome(url, useragent):
    """Автоматизация браузера Chrome, c подменой user-agent"""

    options = webdriver.ChromeOptions()

    options.add_argument(f'user-agent={useragent.random}')

    # подключаем прокси
    options.add_argument('--proxy-server=138.128.91.65:8000')
    driver = webdriver.Chrome(executable_path=WEBDRIVER_PATH_CHROME, options=options)

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