import csv
import re

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent  # pip install fake-useragent

ua = UserAgent()

site = 'https://intecron-msk.ru/stalnie-dveri/gotovie-resheniya.html'
domain = 'https://intecron-msk.ru/'

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


def get_page_data(page):
    articles = {}
    with open(page) as f:
        src = f.read()
        soup = BeautifulSoup(src, 'lxml')
        # with open('intecron.csv', 'w', encoding='UTF-8') as file:
        #     writer = csv.writer(file)
        #     writer.writerow(
        #         (
        #             'Наименование',
        #             'Цена товара',
        #             'Изображение товара',
        #             'Описание товара',
        #             'Внешняя панель(да\нет)',
        #             'Производитель(Фирма производитель)',
        #             'Картинка панель внешняя',
        #             'Панель внешняя название',
        #             'Картинка панель внутренняя',
        #             'Панель внутренняя название',
        #             'Толщина металла',
        #             'Контуры уплотнения',
        #             'Размеры',
        #             'Наполнение двери',
        #             'Стеклопакет(да\нет)',
        #             'Зеркало(да\нет)',
        #             'Терморазрыв(да\нет)',
        #             'Магнитный уплотнитель(да\нет)',
        #             'Галерея',
        #         )
        #     )
        for urls in soup.find_all('div', class_='catalog-item__title'):
            url = urls.find('a').get('href')

            req = requests.get(url, headers=headers)
            src = req.text
            soup = BeautifulSoup(src, 'lxml')
            for item in soup.find('div', id='container'):
                name = item.find('div', class_='txt')
                print(name)
            # articles['Наименование'] = name
            # images = soup.find('div', class_='product-card__img-inner').find_all('a')
            # img_external_panel = domain + images[0].get('href')
            #
            # image = (domain + images[0].get('href'), domain + images[1].get('href'))
            # gallery = [domain + img.find('img').get('src') for img in soup.find_all('div', class_='product-views__item-img')]
            # try:
            #     metal_thickness = soup.find('p', class_='product-features__subtitle').find_next('p').text
            # except:
            #     metal_thickness = None
            # try:
            #     seal_contours = soup.find('p', class_='product-features__subtitle', text=re.compile('контура уплотнения')).text
            # except:
            #     seal_contours = None
            # try:
            #     door_filling = soup.find('p', class_='product-features__subtitle', text=re.compile('Утепление')).find_next('p').text
            # except:
            #     door_filling = None
            # try:
            #     external_panel = soup.find('p', class_='product-features__subtitle', text=re.compile('снаружи')).find_next('p').text
            # except:
            #     external_panel = None
            # try:
            #     for panel in soup.find('div', id='js-product-views').find_all('div', class_='product-views__item-title'):
            #         internal_panel = panel.text.strip()
            #         articles['Панель внутренняя название'] = internal_panel
            #     for item_price in soup.find('div', id='js-product-views').find_all('input'):
            #             price = item_price.attrs['value']
            #     for img in soup.find('div', id='js-product-views').find_all('div', class_='product-views__item-img'):
            #         img_internal_panel = domain + img.find('img').get('src')
            # except:
            #     internal_panel = None
            #     price = None
            #     img_internal_panel = None
            # try:
            #     description = [desc for desc in soup.find('div', class_='product-features__head').find_all('li')]
            # except:
            #     description = None
            # thermal_break = ['Да' if 'терморазрыв' in name else 'Нет']
            # magnetic_seal = None
            # mirror = None
            # glazed_window = None
            # size = None
            # print(articles)
            # with open('intecron.csv', 'a', encoding='UTF-8') as file:
            #     writer = csv.writer(file)
            #     writer.writerow(
            #         (
            #             name,
            #             price,
            #             image,
            #             description,
            #             'Да',
            #             'Intecron',
            #             img_external_panel,
            #             external_panel,
            #             img_internal_panel,
            #             internal_panel,
            #             metal_thickness,
            #             seal_contours,
            #             size,
            #             door_filling,
            #             glazed_window,
            #             mirror,
            #             thermal_break,
            #             magnetic_seal,
            #             gallery,
            #         )
            #     )


def main():
    # get_page(site)
    get_page_data('index.html')


if __name__ == '__main__':
    main()