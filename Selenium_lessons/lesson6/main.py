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

"""
Работа браузера в фоновом режиме (headless). Это позволяет не открывать окно браузера, что значительно сэкономит 
ресурсы. Нужно в том случае, если мы уверены, что наш код работает корректно и мы планируем использовать код 
неоднократно.
"""


def get_html_by_chrome(url):

    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={USERAGENT_CHROME}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    # включить фоновый режим мы можем двумя способами:
    # 1. Передав в опции
    options.add_argument('--headless')
    # 2. Вызвав в опциях и передав True
    options.headless = True
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
        driver.find_element_by_id('l_pr').click()
        time.sleep(5)
        # кликнем по видео
        driver.find_element_by_class_name('VideoPreview__thumbWrap').click()

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
        time.sleep(5)
        # найдем видео
        driver.get('https://www.instagram.com/p/CCsYtgjn1mj/')
        # кликнем по значку с перечеркнутым динамиком
        driver.find_element_by_xpath('***the xpath we need***').click()

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
