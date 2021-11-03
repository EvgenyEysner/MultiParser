import csv
import re

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent  # pip install fake-useragent

ua = UserAgent()

site = 'https://заводскиедвери.рф/catalog/zheleznye_dveri/'
domain = 'https://заводскиедвери.рф'

headers = {
    'User-Agent': ua.random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
}


def get_page(url):
    req = requests.get(url, headers=headers)
    src = req.text

    with open('index.html', 'w') as file:
        index = file.write(src)
    return index


def get_page_data(url):

    product_urls = []
    articles = {}
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    pages = int(soup.find('div', class_='bx-pagination-container row').find('ul').find_all('li')[-2].text)
    with open('factory.csv', 'w', encoding='UTF-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'Наименование',
                'Цена товара',
                'Изображение товара',
                'Описание товара',
                'Внешняя панель(да\нет)',
                'Производитель(Фирма производитель)',
                'Картинка панель внешняя',
                'Панель внешняя название',
                'Картинка панель внутренняя',
                'Панель внутренняя название',
                'Толщина металла',
                'Контуры уплотнения',
                'Размеры',
                'Наполнение двери',
                'Стеклопакет(да\нет)',
                'Зеркало(да\нет)',
                'Терморазрыв(да\нет)',
                'Магнитный уплотнитель(да\нет)',
                'Галерея',
            )
        )

    for page in range(1, pages + 1):  # pages + 1
        page_url = f'https://заводскиедвери.рф/catalog/zheleznye_dveri/?PAGEN_1={page}'
        req = requests.get(page_url, headers=headers)
        res = req.text
        soup = BeautifulSoup(res, 'lxml')
        for urls in soup.find_all('td', class_='gallery-list'):
            items_url = domain + urls.find('a').get('href')
            req = requests.get(items_url, headers=headers)
            res = req.text
            soup = BeautifulSoup(res, 'lxml')

            name = soup.find('h1', attrs={'itemprop': 'name'}).text.strip()
            price = soup.find('div', class_='price-table').find_next('span').text.replace('₽', '')
            img = [domain + image.get('href') for image in soup.find_all('a', attrs={'data-gallery': 'gal-item'})]
            desc = soup.find('div', id='text')
            gallery = None
            external_panel_ = None
            manufacturer = 'ООО "Заводские двери"'
            img_external_panel = img[0]
            img_internal_panel = img[0]
            try:
                metal_thickness = soup.find(text=re.compile('Толщина:')).find_next('td').text.strip()
            except:
                metal_thickness = None
            try:
                seal_contours = soup.find(text=re.compile('Контуров уплотнения:')).find_next('td').text.strip()
            except:
                seal_contours = None
            try:
                size = soup.find(text=re.compile('Размеры по коробу:')).find_next('td').text.strip()
            except:
                size = None
            try:
                door_filling = soup.find(text=re.compile('Утеплитель:')).find_next('td').text.strip()
            except:
                door_filling = None
            try:
                external_panel = soup.find(text=re.compile('Внешняя отделка:')).find_next('td').text.strip()
            except:
                external_panel = None
            external_panel_ = 'Да'
            try:
                internal_panel = soup.find(text=re.compile('Внутренняя отделка:')).find_next('td').text.strip()
            except:
                internal_panel = None
            try:
                glazed_window = ['Да' if 'стекло' in name else 'Нет']
            except:
                glazed_window = None
            try:
                mirror = ['Да' if 'зеркало' in name else 'Нет']
            except:
                mirror = None
            try:
                thermal_break = ['Да' if 'Термо' in name else 'Нет']
            except:
                thermal_break = None
            magnetic_seal = None
            with open('factory.csv', 'a', encoding='UTF-8') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        name,
                        price,
                        img,
                        desc,
                        external_panel_,
                        manufacturer,
                        img_external_panel,
                        external_panel,
                        img_internal_panel,
                        internal_panel,
                        metal_thickness,
                        seal_contours,
                        size,
                        door_filling,
                        glazed_window,
                        mirror,
                        thermal_break,
                        magnetic_seal,
                        gallery,
                    )
                )


def main():
    get_page(site)
    get_page_data(site)


if __name__ == '__main__':
    main()