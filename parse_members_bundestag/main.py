import csv

import requests
from bs4 import BeautifulSoup
import json


URL = 'https://www.bundestag.de/ajax/filterlist/en/members/453158-453158?limit=20&noFilterSet=true&offset='


def get_url_members(url):
    """Забирает ссылки на все страницы членов бундестага и сохраняет их в файл txt"""
    persons_url_list = []
    for i in range(0, 750, 20):
        # методом тыка определили, что членов всего около 740, на странице отображается 20. Забираем все страницы
        # с ссылками
        urls = url + str(i)
        # print(urls)

        qrc = requests.get(urls)
        result = qrc.content

        soup = BeautifulSoup(result, 'lxml')
        persons = soup.find_all(class_="bt-open-in-overlay")

        for person in persons:
            person_page_url = person.get('href')
            persons_url_list.append(person_page_url)

    with open('persons_url_list.txt', 'a', encoding='utf-8') as file:
        for line in persons_url_list:
            file.write(f'{line}\n')


def get_data():

    with open('persons_url_list.txt', encoding='utf-8') as file:

        lines = [line.strip() for line in file.readlines()]

        data_dict = []
        count = 0
        for line in lines:
            qrc = requests.get(line)
            result = qrc.content

            soup = BeautifulSoup(result, 'lxml')
            person = soup.find(class_='bt-biografie-name').find('h3').text
            person_name_fraction = person.strip().split(',')
            person_name = person_name_fraction[0]
            person_fraction = person_name_fraction[1].strip()

            social_networks = soup.find_all(class_='bt-link-extern')

            social_networks_urls = [item.get('href') for item in social_networks]

            data = {
                'person_name': person_name,
                'fraction_name': person_fraction,
                'social_networks': social_networks_urls
            }

            count += 1
            print(f'#{count}: {line} - is done')
            data_dict.append(data)

            with open('data.csv', 'a', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        person_name,
                        person_fraction,
                        social_networks_urls
                    )
                )

            with open('data.json', 'w', encoding='utf-8') as file:
                json.dump(data_dict, file, indent=4, ensure_ascii=False)


def main():
    # get_url_members(URL)
    get_data()


if __name__ == '__main__':
    main()


