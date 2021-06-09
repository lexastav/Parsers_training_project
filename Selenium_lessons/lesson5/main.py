
#  Список опций для Chromium: https://peter.sh/experiments/chromium-command-line-switches/
from selenium import webdriver
import time

from settings import (URL,
                      WEBDRIVER_PATH_FIREFOX,
                      WEBDRIVER_PATH_CHROME,
                      USERAGENT_FIREFOX,
                      USERAGENT_CHROME
                      )

"""Отключение режима webdriver"""


def get_html_by_chrome(url):

    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={USERAGENT_CHROME}')

    # disable webdriver mode

    # for older ChromeDriver under version 79.0.3945.16
    # options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # options.add_experimental_option('useAutomationExtension', False)

    # for ChromeDriver version 79.0.3945.16 or over
    options.add_argument('--disable-blink-features=AutomationControlled')

    driver = webdriver.Chrome(executable_path=WEBDRIVER_PATH_CHROME, options=options)

    try:
        driver.get(url)
        time.sleep(10)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def get_html_by_firefox(url):

    options = webdriver.FirefoxOptions()
    options.set_preference('general.useragent.override', USERAGENT_FIREFOX)
    # disable webdriver mode
    options.set_preference('dom.webdriver.enabled', False)

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
