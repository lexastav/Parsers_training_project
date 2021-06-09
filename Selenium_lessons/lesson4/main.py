from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # нужно что бы эмулировать нажатие клавиши enter
import time

from settings import (URL_VK,
                      URL_INSTAGRAM,
                      WEBDRIVER_PATH_FIREFOX,
                      WEBDRIVER_PATH_CHROME,
                      USERAGENT_FIREFOX,
                      USERAGENT_CHROME
                      )

from auth_data import LOGIN_VK, LOGIN_INST, PASSWORD_VK, PASSWORD_INST
import pickle

"""Авторизация и заполнение форм на примере instagram и vk сохранением cookies"""


def get_html_by_chrome(url):
    """Автоматизация браузера Chrome, c подменой user-agent"""

    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={USERAGENT_CHROME}')
    driver = webdriver.Chrome(executable_path=WEBDRIVER_PATH_CHROME, options=options)

    try:
        driver.get(url)
        time.sleep(5)

        email_input = driver.find_element_by_id('index_email')
        email_input.clear()
        email_input.send_keys(LOGIN_VK)
        time.sleep(5)

        password_input = driver.find_element_by_id('index_pass')
        password_input.clear()
        password_input.send_keys(PASSWORD_VK)
        time.sleep(5)

        # можем кликнуть по кнопке login
        driver.find_element_by_id('index_login_button').click()

        # перейдем сразу на ленту новостей, это может пригодиться если вылезет какое-либо окно с просьбой подтвердить
        # данные или еще чего
        driver.find_element_by_id('l_news').click()

        # сохраним cookies
        pickle.dump(driver.get_cookies(), open(f'{LOGIN_VK}cookies', 'wb'))

        # подгрузм cookies и можем их использовать в дальнейшем
        def load_cookies(url):
            driver.get(url)
            time.sleep(5)

            for cookie in pickle.load(open(f'{LOGIN_VK}cookies', 'rb')):
                driver.add_cookie(cookie)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def get_html_by_firefox(url):
    """Автоматизация браузера FireFox, c подменой user-agent"""

    options = webdriver.FirefoxOptions()

    options.set_preference('general.useragent.override', USERAGENT_FIREFOX)

    driver = webdriver.Firefox(executable_path=WEBDRIVER_PATH_FIREFOX, options=options)

    try:
        driver.get(url)
        time.sleep(5)

        username_input = driver.find_element_by_name('username')
        username_input.clear()
        username_input.send_keys(LOGIN_INST)
        time.sleep(5)

        password_input = driver.find_element_by_name('password')
        password_input.clear()
        password_input.send_keys(PASSWORD_INST)
        time.sleep(5)
        # можем отправить форму, эмулировав нажатие enter, в данном случае это будет логичнее и проще, так как у кнопки
        # login нет уникальных атрибутов, за которые можно заципиться что бы ее кликнуть
        password_input.send_keys(Keys.ENTER)

        # сохраним cookies
        pickle.dump(driver.get_cookies(), open(f'{LOGIN_INST}cookies', 'wb'))

        # подгрузм cookies и можем их использовать в дальнейшем
        def load_cookies(url):
            driver.get(url)
            time.sleep(5)

            for cookie in pickle.load(open(f'{LOGIN_INST}cookies', 'rb')):
                driver.add_cookie(cookie)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def main():
    get_html_by_chrome(URL_VK)
    get_html_by_firefox(URL_INSTAGRAM)


if __name__ == '__main__':
    main()
