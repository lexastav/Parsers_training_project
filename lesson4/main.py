import requests
from bs4 import BeautifulSoup
import json

# from proxy_auth import PROXIES


HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37'
    }

URL_PREF = 'https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=2%20Jun%202021&to_' \
      'date=&genre%5B%5D=pop&maxprice=500&o='
URL_POSTF = '&bannertitle=July'


def get_urls_list(url_pref, url_postf, headers):
    """
    Собирает все ссылки фестивалей со страницы
    :param url_pref: часть url get-запроса до параметра пагинации
    :param url_postf: часть url get-запроса после параметра пагинации
    :param headers: прикидываемся браузером
    :return: Список всех url фестивалей
    """

    fest_urls_list = []
    for i in range(0, 51, 24):
        url = f'{url_pref}{str(i)}{url_postf}'

        req = requests.get(url, headers)  # возможно потребуется прокси, тогда после headers надо будет
        # добавить proxies=PROXIES. PROXIES мы импортировали из соседнего файла, который специально создали для
        # хранения всех прокси.

        json_data = json.loads(req.text)
        html_response = json_data['html']

        with open(f'data/index_{i}.html', 'w', encoding='utf-8') as file:
            file.write(html_response)

        with open(f'data/index_{i}.html') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        cards = soup.find_all('a', class_='card-details-link')

        for item in cards:
            fest_urls_list.append('https://www.skiddle.com' + item.get('href'))

    return fest_urls_list

# print(get_urls_list(URL_PREF, URL_POSTF, HEADERS))


def get_fest_info(url_lst):
    """
    Забираем всю инфу по фестивалям
    :param url_lst: список ссылок на фестивали (например результат работы предыдущей функции)
    :return: Список всех собранных данных: название, дата, контактная информация в виде словаря
    """
    count = 0
    fest_list_result = []
    for url in url_lst:
        count += 1
        print(count, url, sep='\n')

        req = requests.get(url, HEADERS)  # возможно потребуется прокси, тогда после headers надо будет
        # добавить proxies=PROXIES. PROXIES мы импортировали из соседнего файла, который специально создали для
        # хранения всех прокси.

        try:
            soup = BeautifulSoup(req.text, 'lxml')
            fest_info_block = soup.find('div', class_='top-info-cont')

            fest_name = fest_info_block.find('h1').text.strip()
            fest_date = fest_info_block.find('h3').text.strip()
            fest_location_url = 'https://www.skiddle.com' + fest_info_block.find('a', class_='tc-white').get('href')
            # print(fest_name, fest_date, fest_location_url, sep='\n')

            req = requests.get(fest_location_url, HEADERS)  # возможно потребуется прокси, тогда после headers надо
            # будет добавить proxies=PROXIES. PROXIES мы импортировали из соседнего файла, который специально создали
            # для хранения всех прокси.
            soup = BeautifulSoup(req.text, 'lxml')
            contact_details = soup.find('h2', string='Venue contact details and info').find_next()

            items = [item.text for item in contact_details.find_all('p')]

            # Собирем контактную информацию в словарь
            contact_details_dict = {}
            for contact_detail in items:
                # разделителем будет ':'
                contact_details_list = contact_detail.split(':')
                # но мы столкнулись с проблемой, в ссылке тоже есть двоеточие, решим эту проблему следующим образом
                if len(contact_details_list) == 3:
                    contact_details_dict[contact_details_list[0].strip()] = contact_details_list[1].strip() + ':'\
                                                                            + contact_details_list[2].strip()
                else:
                    contact_details_dict[contact_details_list[0].strip()] = contact_details_list[1].strip()
                # print(contact_detail)

            fest_list_result.append(
                {
                    'Fest_name': fest_name,
                    'Fest_date': fest_date,
                    'Contacts_data': contact_details_dict
                }
            )

        except Exception as ex:
            print(ex, 'Damn... There was some error...', sep='\n')

    return fest_list_result


def main():
    with open('fest_list_result.json', 'w', encoding='utf-8') as file:
        json.dump(get_fest_info(get_urls_list(URL_PREF, URL_POSTF, HEADERS)), file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()