import requests
import img2pdf

HEADERS = {
    'Accept': 'image/webp,*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'
}

URL = 'http://www.recordpower.co.uk/flip/Winter2020/files/mobile/'


def get_data(base_url, headers):

    for i in range(1, 49):
        url = base_url + str(i) + '.jpg'
        req = requests.get(url, headers)
        response = req.content

        with open(f'media/{i}.jpg', 'wb') as file:
            file.write(response)
            print(f'downloaded {i} of 48')


def jpg_to_pdf():
    with open('media/result.pdf', 'wb') as file:
        file.write(img2pdf.convert([f'media/{i}.jpg' for i in range(1, 49)]))


def main():
    # get_data(URL, HEADERS)
    jpg_to_pdf()


if __name__ == '__main__':
    main()