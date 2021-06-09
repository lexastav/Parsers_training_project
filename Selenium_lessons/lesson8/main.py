from selenium import webdriver
import time
from multiprocessing import Pool

from settings import (URLS_LIST,
                      WEBDRIVER_PATH_FIREFOX,
                      WEBDRIVER_PATH_CHROME,
                      USERAGENT_FIREFOX,
                      USERAGENT_CHROME
                      )


"""Запуск нескольких браузеров одновременно (Multiprocessing)"""


def get_data_by_chrome(url: list):
    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={USERAGENT_CHROME}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    # options.headless = True
    driver = webdriver.Chrome(executable_path=WEBDRIVER_PATH_CHROME, options=options)
    try:
        driver.get(url)
        time.sleep(5)
        driver.get_screenshot_as_file(f'media/{url.split("//")[1]}.png')
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()



def get_html_by_firefox(url):

    options = webdriver.FirefoxOptions()
    options.set_preference('general.useragent.override', USERAGENT_FIREFOX)
    options.set_preference('dom.webdriver.enabled', False)
    # headless mode
    options.headless = True
    driver = webdriver.Firefox(executable_path=WEBDRIVER_PATH_FIREFOX, options=options)

    try:
        pass
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


if __name__ == '__main__':
    p = Pool(processes=len(URLS_LIST))
    p.map(get_data_by_chrome, URLS_LIST)
