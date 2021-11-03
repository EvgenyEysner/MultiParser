import csv
import re
import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent  # pip install fake-useragent

ua = UserAgent()

site = 'https://dveri.com/catalog/vhodnye-dveri'
domain = 'https://dveri.com'

headers = {
    'User-Agent': ua.random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
}

proxies1 = {
    'http': 'http://Uv37g8nf:yjTQ5xs7@84.246.84.164:46471',
    'https': 'http://Uv37g8nf:yjTQ5xs7@84.246.84.164:46471',
}
proxies2 = {
    'http': 'http://Uv37g8nf:yjTQ5xs7@84.246.86.183:54536',
    'https': 'http://Uv37g8nf:yjTQ5xs7@84.246.86.183:54536',
}
proxies3 = {
    'http': 'http://Uv37g8nf:yjTQ5xs7@84.246.109.182:56688',
    'https': 'http://Uv37g8nf:yjTQ5xs7@84.246.109.182:56688',
}
proxies4 = {
    'http': 'http://Uv37g8nf:yjTQ5xs7@2.56.136.96:59907',
    'https': 'http://Uv37g8nf:yjTQ5xs7@2.56.136.96:59907',
}
proxies5 = {
    'http': 'http://Uv37g8nf:yjTQ5xs7@2.57.150.4:51578',
    'https': 'http://Uv37g8nf:yjTQ5xs7@2.57.150.4:51578',
}


def get_page(url):
    req = requests.get(url, headers=headers)
    src = req.text

    with open('index.html', 'w') as file:
        index = file.write(src)
    return index


def get_page_data(url):
    with open('bravo.csv', 'w', encoding='UTF-8') as file:
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

    product_urls = []
    # articles = []
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    pages = int(soup.find('ul', class_='pagination').find_all('a', class_='pagination__link')[-1].text)
    for page in range(1, pages + 1):  # pages + 1
        page_url = f'https://dveri.com/catalog/vhodnye-dveri?page={page}'
        req = requests.get(page_url, headers=headers)
        res = req.text
        soup = BeautifulSoup(res, 'lxml')
        for urls in soup.find_all('div', class_='products__item'):
            items_url = domain + urls.find('a', class_='card').get('href')
            product_urls.append(items_url)

            req = requests.get(items_url, headers=headers)
            res = req.text
            soup = BeautifulSoup(res, 'lxml')
            name = soup.find('div', class_='product__tablet-title').text
            panels = soup.find('div', class_='product__tablet-collection').text.split('/')

            price = soup.find('div', class_='product__price').text.replace('₽', '').strip()
            img_1 = domain + soup.find('div', class_='product__img-wrap').find('img').get('src')
            img_2 = domain + soup.find('div', class_='product__img-wrap').find('img').find_next('img').get('src')
            img = (img_1, img_2)
            try:
                description = soup.find('div', class_='product__property-list')
            except:
                description = None
            try:
                metal_thickness = soup.find('div', class_='product__property-name',
                                                text=re.compile('Толщина стали')).find_next('div',
                                                                                            class_='product__property-value').text
            except:
                metal_thickness = None
            try:
                seal_contours = soup.find('div', class_='product__property-name',
                                              text=re.compile('Уплотнение')).find_next('div',
                                                                           class_='product__property-value').text
            except:
                seal_contours = None
            try:
                size = soup.find('div', class_='product__property-name', text=re.compile('Размер')).find_next('div',
                                                                                                                  class_='product__property-value').text
            except:
                size = None
            try:
                door_filling = soup.find('div', class_='product__property-name',
                                             text=re.compile('Утепление')).find_next('div',
                                                                                     class_='product__property-value').text
            except:
                door_filling = None
            try:
                external_panel = panels[0]
            except:
                external_panel = None
            img_external_panel = img_1
            try:
                internal_panel = panels[1]
            except:
                internal_panel = None
            try:
                outside = soup.find('div', class_='product__property-name', text=re.compile('Отделка снаружи')).find_next('div', class_='product__property-value').text
            except:
                outside = None
            try:
                inside = soup.find('div', class_='product__property-name', text=re.compile('Отделка внутри')).find_next('div', class_='product__property-value').text
            except:
                inside = None
            external_panel_ = ['Нет' if 'металл' in outside else 'Да']
            img_internal_panel = img_2
            glazed_window = ['Да' if 'стекло' in inside else 'Нет']
            mirror = ['Да' if 'зеркало' in internal_panel else 'Нет']
            thermal_break = ['Да' if 'терморазрыв' in internal_panel else 'Нет']
            magnetic_seal = ['Да' if 'магнит' in internal_panel else 'Нет']

            time.sleep(2)
            with open('bravo.csv', 'a', encoding='UTF-8') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        name,
                        price,
                        img,
                        description,
                        external_panel_,
                        'Фабрика дверей BRAVO',
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
                        None,
                    )
                )


def main():
    # get_page(site)
    get_page_data(site)


if __name__ == '__main__':
    main()
