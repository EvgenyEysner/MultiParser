import csv
import re
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent  # pip install fake-useragent

ua = UserAgent()

site = 'https://argusmsk.ru/page/vnutrennie-paneli'
domain = 'https://argusmsk.ru'

headers = {
    'User-Agent': ua.random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
}


def make_request(url):
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    return soup


def get_page(url):
    req = requests.get(url, headers=headers)
    src = req.text

    with open('index_internal.html', 'w') as file:
        index = file.write(src)
    return index


def get_page_data(page):
    with open('internal_panel.csv', 'w', encoding='UTF-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'Наименование',
                'Изображение товара',
                'Панель внутренняя название',
            )
        )
    with open(page) as f:
        src = f.read()
        soup = BeautifulSoup(src, 'lxml')

        i_panels = soup.find_all(text=re.compile('Возможные цвета'))
        for item in i_panels:
            name = item.find_previous('span').text.replace('"', '').strip()
            image = item.find_previous('a', class_='colorbox').get('href')
            for color_item in item.find_previous('td').text.split(':')[1].replace('\n\t\t\t', '').replace('----', '').split('-'):
                color = color_item

                with open('internal_panel.csv', 'a', encoding='UTF-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(
                        (
                            name,
                            image,
                            color,
                        )
                    )


def main():
    get_page(site)
    get_page_data('index_internal.html')


if __name__ == '__main__':
    main()