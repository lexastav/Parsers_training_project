"""
Парсим health-diet.ru
"""

import requests
from bs4 import BeautifulSoup
import json

URL = 'https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'

HEADERS = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37'
}


def get_index_page():

    """Тащит нужную нам страницу по указанному url"""

    req = requests.get(URL, headers=HEADERS)
    src = req.text
    # print(src)

    with open('index.html', 'w', encoding='utf-8') as file:
        return file.write(src)


def get_all_categories_json():

    """Достает ссылки на категории и сохраняет их в json"""

    with open('index.html', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    all_products_hrefs = soup.find_all(class_="mzr-tc-group-item-href")

    all_categories_dict = {}
    for item in all_products_hrefs:
        item_text = item.text
        item_href = 'https://health-diet.ru' + item.get("href")
        # print(f'{item_text} : {item_href}')
        all_categories_dict[item_text] = item_href

    with open('all_categories_dict.json', 'w', encoding='utf-8') as file:
        return json.dump(all_categories_dict, file, indent=4,  ensure_ascii=False)


with open('all_categories_dict.json', encoding='utf-8') as file:
    all_categories = json.load(file)
    # print(all_categories)

for category_name, category_href in all_categories.items():

    rep = [',', ' ', '-', "'"]
    for item in rep:
        if item in category_name:
            category_name = category_name.replace(item, '_')
    # print(category_name)

    req = requests.get(url=category_href)






