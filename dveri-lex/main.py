import csv
import re
import time
from random import choice

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent  # pip install fake-useragent

user = UserAgent().random

site = 'http://dveri-lex.ru/category/dveri/'
domain = 'http://dveri-lex.ru'

headers = {
    'User-Agent': user,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
}

# with open('proxy.txt') as file:
#     proxy_base = ''.join(file.readlines()).strip().split('\n')
#     for proxy in proxy_base:
#
#         proxies = {
#             'http': f'http://{proxy}',
#             'https': f'https://{proxy}'
#         }


def get_index(url):
    req = requests.get(url, headers=headers)
    print(f'IP: {req}')
    src = req.text

    with open('index.html', 'w') as file:
        index = file.write(src)
    return index


def pagination(page):
    with open(page) as f:
        src = f.read()
        soup = BeautifulSoup(src, 'lxml')
    pages = int(soup.find('ul', class_='menu-h').find_all('li')[-2].text)
    return pages


def get_page_data(pages):
    with open('lex.csv', 'w', encoding='UTF-8') as file:
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
    item_links = []

    for page in range(1, pages + 1):  # pages + 1
        page_url = f'http://dveri-lex.ru/category/dveri/?page={page}'
        print(page_url)
        req = requests.get(page_url, headers=headers)
        res = req.text
        soup = BeautifulSoup(res, 'lxml')
        for urls in soup.find_all('div', class_='pl-item-image'):
            items_url = domain + urls.find('a').get('href')
            item_links.append(items_url)

            req = requests.get(f'{items_url}', headers=headers)
            res = req.text
            soup = BeautifulSoup(res, 'lxml')

            name = soup.find('h1').find('span', attrs={'itemprop': 'name'}).text.strip()
            price = soup.find('div', class_='price-wrapper').find('span', class_='price nowrap').text.split('Р')[0].strip()
            image = domain + soup.find('img', id='product-image').get('src')
            desc = soup.find('div', id='product-description')
            try:
                external_panel_ = ['Нет' if 'металл' in external_panel_name or external_panel_name_1 else 'Да']
            except:
                external_panel_ = None
            manufacturer = 'Лекс'
            img_external_panel = image
            try:
                external_panel_name_1 = soup.find(text=re.compile('Отделка снаружи')).find_parent('p').text.split(':')[1].strip()
            except:
                external_panel_name_1 = None

            try:
                external_panel_name = soup.find(text=re.compile('Внешняя отделка')).find_next().text.strip()
            except:
                external_panel_name = None


            img_internal_panel = image
            try:
                internal_panel_name_1 = soup.find(text=re.compile('Отделка внутри')).find_parent('p').text.split(':')[1]
            except:
                internal_panel_name_1 = None
            try:
                internal_panel_name = soup.find(text=re.compile('Внутренняя отделка')).find_next().text.strip()
            except:
                internal_panel_name = None
            # print(internal_panel_name_1, internal_panel_name)
            try:
                metal_thickness = soup.find(text=re.compile('Дверное полотно')).find_parent('p').text.split(':')[1]
            except:
                metal_thickness = None
            try:
                seal_contours = soup.find(text=re.compile('Уплотнитель')).find_parent('p').text.split(':')[1]
            except:
                seal_contours = None
            try:
                size = soup.find('li', text=re.compile('ширина')).text.strip().replace(';', '').replace(',', '/')
            except:
                size = None
            try:
                door_filling = soup.find(text=re.compile('Утепление')).next_sibling.text.strip()
            except:
                door_filling = None
            try:
                glazed_window = ['Да' if 'стекло' in internal_panel_name or internal_panel_name_1 else 'Нет']
            except:
                glazed_window = None
            try:
                mirror = ['Да' if 'зеркало' in name else 'Нет']
            except:
                mirror = None
            try:
                thermal_break = ['Да' if 'терморазрыв' in name else 'Нет']
            except:
                thermal_break = None
            try:
                magnetic_seal = ['Да' if 'магнит' in internal_panel_name else 'Нет']
            except:
                magnetic_seal = None
            try:
                gallery = [domain + img.get('href') for img in soup.find('div', id='product-gallery').find_all('a')]
            except:
                gallery = None
            with open('lex.csv', 'a', encoding='UTF-8') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        name,
                        price,
                        image,
                        desc,
                        external_panel_,
                        manufacturer,
                        img_external_panel,
                        [external_panel_name or external_panel_name_1],
                        img_internal_panel,
                        [internal_panel_name or internal_panel_name_1],
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
    get_index(site)
    pagination('index.html')
    get_page_data(pagination('index.html'))


if __name__ == '__main__':
    main()