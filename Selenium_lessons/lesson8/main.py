from selenium import webdriver
import time
from multiprocessing import Pool
from random import randrange

from settings import (URLS_LIST,
                      URL,
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


def get_data_by_firefox(url):
    """На примере firefox покажем как реализовать мультипроцессинг на одном url, на примере tiktok"""
    options = webdriver.FirefoxOptions()
    options.set_preference('general.useragent.override', USERAGENT_FIREFOX)
    options.set_preference('dom.webdriver.enabled', False)
    # headless mode
    # options.headless = True
    driver = webdriver.Firefox(executable_path=WEBDRIVER_PATH_FIREFOX, options=options)

    try:
        driver.find_element_by_xpath('//*[@id="main"]/div[3]/div[2]/div/div[1]/span[1]/div/div/div[5]/div[1]/a').click()
        time.sleep(randrange(3, 10))
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


if __name__ == '__main__':
    # p = Pool(processes=len(URLS_LIST))  # создадим объект Pool в аргуметро укажем количество процессов, в нашем
    # случае- это длина списка с url, но можем указать просто какое-нибудь число
    # p.map(get_data_by_chrome, URLS_LIST)  # в метод map передаем нашу функцию, т. е. вызываем ее на списке url.
    # Откроется несколько окон брраузера, в нашем случае 3. Вот и вся магия.

    process_count = int(input('Enter the count of process: '))  # запросим от пользователя количество процессов
    url_list = [URL] * process_count  # создадим список умнодив наш url на количество процессов, т.е. мы получим
    # список из одинаковых url.
    # ну а дальше все как в примере с chrome
    p = Pool(processes=process_count)
    p.map(get_data_by_firefox, url_list)
