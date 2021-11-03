import csv
import re

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent  # pip install fake-useragent

ua = UserAgent()

site = 'https://intecron-msk.ru/mezhkomnatnie-dveri/v-nalichii.html'
domain = 'https://intecron-msk.ru'

headers = {
    'User-Agent': ua.random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
}


def get_page(url):
    req = requests.get(url, headers=headers)
    src = req.text

    with open('intecron/index.html', 'w') as file:
        index = file.write(src)
    return index


def get_page_data(page):

    with open(page) as f:
        src = f.read()
        soup = BeautifulSoup(src, 'lxml')
        with open('intecron/intecron.csv', 'w', encoding='UTF-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    'Наименование',
                    'Цена товара',
                    'Изображение товара',
                    'Описание товара',
                    'Галерея',
                    'Внешняя панель(да\нет)',
                    'Производитель(Фирма производитель)',
                    'Картинка панель внешняя',
                    'Картинка панель внутренняя',
                    'Толщина металла',
                    'Контуры уплотнения',
                    'Размеры',
                    'Наполнение двери',
                    'Панель внешняя',
                    'Панель внутренняя',
                    'Стеклопакет(да\нет)',
                    'Зеркало(да\нет)'
                    'Терморазрыв(да\нет)',
                    'Магнитный уплотнитель(да\нет)',
                )
            )
        for urls in soup.find_all('div', class_='catalog-item__title'):
            url = urls.find('a').get('href')
            req = requests.get(url, headers=headers)
            src = req.text
            soup = BeautifulSoup(src, 'lxml')

            name = soup.find('h1').text
            images = soup.find('div', class_='product-card__img-inner').find_all('a')
            img_external_panel = domain + images[0].get('href')
            img_internal_panel = domain + images[1].get('href')
            image = (domain + images[0].get('href'), domain + images[1].get('href'))
            price = soup.find('strong', id='itemPrice').text.strip()
            gallery = [domain + img.find('img').get('src') for img in soup.find_all('div', class_='product-views__item-img')]
            try:
                metal_thickness = soup.find('div', class_='product-features__item').find_next('p').text
            except:
                None
            try:
                seal_contours = soup.find('p', class_='product-features__subtitle', text=re.compile('контура')).text
            except:
                'Нет'
            try:
                door_filling = soup.find('p', class_='product-features__subtitle', text=re.compile('Утепление')).find_next('p').text
            except:
                'Нет'
            try:
                external_panel = soup.find('p', class_='product-features__subtitle', text=re.compile('снаружи')).find_next('p').text
            except:
                'Нет'
            try:
                internal_panel = soup.find('p', class_='product-features__subtitle', text=re.compile('Отделка изнутри')).find_next('p').text
            except:
                'Нет'
            try:
             description = [desc.text.strip() for desc in soup.find('div', class_='product-features__head').find_all('li')]
            except:
                'Нет'
            thermal_break = None
            magnetic_seal = None
            mirror = None
            glazed_window = None
            size = None
            # print(internal_panel)
            with open('intecron/intecron.csv', 'a', encoding='UTF-8') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        name,
                        price,
                        image,
                        description,
                        gallery,
                        'Да',
                        'INTECRON',
                        img_external_panel,
                        img_external_panel,
                        metal_thickness,
                        seal_contours,
                        size,
                        door_filling,
                        external_panel,
                        internal_panel,
                        glazed_window,
                        mirror,
                        thermal_break,
                        magnetic_seal,
                    )
                )


def main():
    # get_page(site)
    get_page_data('intecron/index.html')


if __name__ == '__main__':
    main()