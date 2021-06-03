import csv
import json
import os
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

URL = 'https://shop.casio.ru/catalog/g-shock/filter/gender-is-male/apply/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37'
}


def get_page(url, headers):
    """получает одну страницу на посмотреть"""
    req = requests.get(url, headers)

    if not os.path.exists('data'):
        os.mkdir('data')

    with open('data/page_1.html', 'w', encoding='utf-8') as file:
        file.write(req.text)


def get_all_pages():
    """Стаскивает все страницы с учетом параметра пагинации"""
    with open('data/page_1.html', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    # достанем количество страниц, в принципе ничто нам не мешает в ручную это посмотреть, но сделаем это в коде
    # важный момент! блок с пагинацией есть в скаченной странице, а в странице оригинальной его нет!
    pages_count = int(soup.find('div', class_='bx-pagination-container').find_all('a')[-2].text)

    for i in range(1, pages_count + 1):
        url = f'https://shop.casio.ru/catalog/g-shock/filter/gender-is-male/apply/?user-agent=Mozilla%2F5.0+%28' \
              f'Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+' \
              f'Chrome%2F91.0.4472.77+Safari%2F537.36+Edg%2F91.0.864.37&PAGEN_1={i}'

        # не используем user-agent так как он уже указан в ссылке
        req = requests.get(url)

        with open(f'data/page_{i}.html', 'w', encoding='utf-8') as file:
            file.write(req.text)

        time.sleep(2)


def collect_data():
    """Собирает нужные данные с сохраненных вебстраниц"""
    cur_date = datetime.now().strftime('%d_%m_%Y')

    with open(f'data_{cur_date}.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'product_article',
                'product_price',
                'product_url'
            )
        )

    data = []
    for page in range(1, len(os.listdir(path="data")) + 1):
        with open(f'data/page_{page}.html', encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        items_cards = soup.find_all('a', class_='product-item__link')

        for item in items_cards:
            product_article = item.find('p', class_='product-item__articul').text.strip()
            product_price = item.find('p', class_='product-item__price').text.lstrip('руб. ')
            product_url = 'https://shop.casio.ru' + item.get('href')
            data.append(
                {
                    'product_article': product_article,
                    'product_price': product_price,
                    'product_url': product_url
                }
            )

            with open(f'data_{cur_date}.csv', 'a', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        product_article,
                        product_price,
                        product_url
                    )
                )

        print(f'Обрабатывается страница: {page} из {len(os.listdir(path="data"))}')

    with open(f'data_{cur_date}.json', 'a', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def main():
    # get_page(URL, HEADERS)
    # get_all_pages()
    collect_data()


if __name__ == '__main__':
    main()