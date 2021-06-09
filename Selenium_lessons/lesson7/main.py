from selenium import webdriver
import time
from datetime import datetime

from settings import (URL,
                      WEBDRIVER_PATH_FIREFOX,
                      WEBDRIVER_PATH_CHROME,
                      USERAGENT_FIREFOX,
                      USERAGENT_CHROME
                      )


"""Переключение между вкладками на примере авито и implicitly_wait()"""


def get_html_by_chrome(url):

    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={USERAGENT_CHROME}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    # options.headless = True
    driver = webdriver.Chrome(executable_path=WEBDRIVER_PATH_CHROME, options=options)

    try:
        start_time = datetime.now()
        # прыгаем на ссылку нужной нам категории
        driver.get(url)
        print(f'Currently URL is: {driver.current_url}')
        time.sleep(5)
        # получаем список всех товаров на странице,
        items = driver.find_elements_by_xpath('//div[@data-marker="item-photo"]')
        # посмотрим на количество элементов
        print(len(items))
        # кликнем на первый и он откроется в новой вкладке
        items[0].click()
        time.sleep(5)
        #  а так можно переключаться между вкладками
        driver.switch_to.window(driver.window_handles[1])
        print(f'Currently URL is: {driver.current_url}')
        # попробуем спарсить имя продавца
        username = driver.find_element_by_class_name('seller-info-name')
        print(username.text)
        # после не забываем закрыть драйвер и переключиться на другую вкладку, иначе вылезет исключение
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        print(f'Currently URL is: {driver.current_url}')
        # обратимся к другому элементу и спарсим еще что-нибудь, у нас откроется новая вкладка
        items[1].click()
        time.sleep(5)

        # перемещаемся к ней
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(5)
        print(f'Currently URL is: {driver.current_url}')
        username = driver.find_element_by_xpath('//div[@data-marker="seller-info/name"]')

        # заберем дату публикации объявления
        ad_date = driver.find_element_by_class_name('title-info-metadata-item-redesign')

        # а вот дата регистрации пользователя лежит в классе у которого есть еще несколько объектов, но на нашу удачу
        # порядок объектов этого класса всегда постоянный вне зависимости от страницы, в нашем случае дата регистрации-
        # это второй объект.
        joined_date = driver.find_elements_by_class_name('seller-info-value')[1]
        print(username.text, ad_date.text, joined_date.text, sep='\n')
        finish_time = datetime.now()
        print(finish_time - start_time)

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
        start_time = datetime.now()
        # прыгаем на ссылку нужной нам категории
        driver.get(url)
        print(f'Currently URL is: {driver.current_url}')
        driver.implicitly_wait(5)  # очень полезный модуль, в отличии от sleep(), он не ждет все время, то есть если
        # наша страница загрузится за 1 секунду, программа перейдет к выполнению другой процедуры, а не будет ждать все
        # секунды в скобках, может значительно ускорить выполнение скрипта.
        # получаем список всех товаров на странице,
        items = driver.find_elements_by_xpath('//div[@data-marker="item-photo"]')
        # посмотрим на количество элементов
        print(len(items))
        # кликнем на первый и он откроется в новой вкладке
        items[0].click()
        driver.implicitly_wait(5)
        #  а так можно переключаться между вкладками
        driver.switch_to.window(driver.window_handles[1])
        print(f'Currently URL is: {driver.current_url}')
        # попробуем спарсить имя продавца
        username = driver.find_element_by_class_name('seller-info-name')
        print(username.text)
        # после не забываем закрыть драйвер и переключиться на другую вкладку, иначе вылезет исключение
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        print(f'Currently URL is: {driver.current_url}')
        # обратимся к другому элементу и спарсим еще что-нибудь, у нас откроется новая вкладка
        items[1].click()
        driver.implicitly_wait(5)

        # перемещаемся к ней
        driver.switch_to.window(driver.window_handles[1])
        driver.implicitly_wait(5)
        print(f'Currently URL is: {driver.current_url}')
        username = driver.find_element_by_xpath('//div[@data-marker="seller-info/name"]')

        # заберем дату публикации объявления
        ad_date = driver.find_element_by_class_name('title-info-metadata-item-redesign')

        # а вот дата регистрации пользователя лежит в классе у которого есть еще несколько объектов, но на нашу удачу
        # порядок объектов этого класса всегда постоянный вне зависимости от страницы, в нашем случае дата регистрации-
        # это второй объект.
        joined_date = driver.find_elements_by_class_name('seller-info-value')[1]
        print(username.text, ad_date.text, joined_date.text, sep='\n')
        finish_time = datetime.now()
        print(finish_time - start_time)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

def main():
    get_html_by_chrome(URL)
    get_html_by_firefox(URL)


if __name__ == '__main__':
    main()