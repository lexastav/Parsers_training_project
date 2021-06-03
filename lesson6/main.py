# парсинг данных с сайта с "защитой от парсинга"
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

URL = 'https://www.tury.ru/hotel/most_luxe.php'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/'
              'webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru,en-GB;q=0.9,en;q=0.8,en-US;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37'

    }


def get_data(url, headers):
    """получим данные с нужной страницы"""
    req = requests.get(url, headers)
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(req.text)
    # однако, получая страницу классическим способом, мы обнаружим, что нужных данных на ней нет.
    # Поковыряв вкладку "Сеть" в панели разработчика в браузере мы видим некий запрос, пройдя по которому мы
    # обнаруживаем нужные нам данные, используем эту ссылку для запроса.
    req = requests.get('https://api.rsrv.me/hc.php?a=hc&most_id=1317&l=ru&sort=most', headers)
    soup = BeautifulSoup(req.text, 'lxml')

    # парсим данные
    hotels_cards = soup.find_all('div', class_='hotel_card_dv')
    for hotel_url in hotels_cards:
        hotel_url = hotel_url.find('a').get('href')
        print(hotel_url)  # выводим в терминал все полученные данные


""" 
Мы можем проделать то же самое не ковыряя панель разработчика, используя Selenium.
Иногда случается, что ковыряния в панели разработчика ни кчему не приводят, или на это уходит слишком много времени.
В таком случае гораздо более эффективным решение будет автоматизировать работу браузера с помощью вебдрайвера и получить
желаемую страницу
"""


def get_data_with_selenium(url):
    """Скачивает нужную страницу с помощью Selenium"""
    options = webdriver.FirefoxOptions()
    options.set_preference(
        'general.useragent.override',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37'
    )
    try:
        driver = webdriver.Firefox(
            executable_path='C:\\Users\\lexas\\MyDjangoProjects\\Parsers_training_project\\lesson6\\geckodriver.exe',
            options=options
        )
        driver.get(url)
        time.sleep(10)

        with open('index_selenium.html', 'w', encoding='utf-8') as file:
            file.write(driver.page_source)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def get_data_from_index_selenium_html():
    """ Парсит страницу """
    with open('index_selenium.html', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    hotels_cards = soup.find_all('div', class_='hotel_card_dv')
    for hotel_url in hotels_cards:
        hotel_url = f'https://www.tury.ru{hotel_url.find("a").get("href")}'
        print(hotel_url)


def main():
    # get_data(URL, HEADERS)
    # get_data_with_selenium(URL)
    get_data_from_index_selenium_html()


if __name__ == '__main__':
    main()