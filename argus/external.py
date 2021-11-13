import csv
import re
import time
import itertools
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent  # pip install fake-useragent
from selenium import webdriver
from selenium.webdriver.common.by import By

# options = webdriver.FirefoxOptions()
# options.set_preference('dom.webdriver.enabled', False)
ua = UserAgent()
# options.add_argument(ua.random)
# options.add_argument('--headless')
# browser = webdriver.Firefox(executable_path='/home/evgeny/PycharmProjects/MultiParser/geckodriver', options=options)
site = 'https://argusmsk.ru/page/vneshnie-paneli-0'
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

    with open('index_external.html', 'w') as file:
        index = file.write(src)
    return index


def get_page_data(page):
    with open('external_panel.csv', 'w', encoding='UTF-8') as file:
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
        e_panels = soup.find('div', class_='media-body').find_all(text=re.compile('Цвет'))

        for item in e_panels:
            name = item.find_previous('td').text.split()[1].replace('»+', '').replace('»', '').replace('«', '')
            image = item.find_previous('a', class_='colorbox').get('href')
            color = item.find_all_previous('span')[1].text.split(':')[1].replace('.', '')

            with open('external_panel.csv', 'a', encoding='UTF-8') as file:
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
    get_page_data('index_external.html')


if __name__ == '__main__':
    main()