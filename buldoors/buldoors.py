import csv
import random
import re
import time
from random import choice

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent  # pip install fake-useragent
from selenium import webdriver
from selenium.webdriver.common.by import By

user = UserAgent().random

site = 'https://buldoors-moscow.ru/product-category/doors-buldoors/'
domain = 'https://buldoors-moscow.ru'

headers = {
    'User-Agent': user,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
}


# with open('proxy.txt') as f:
#     proxy_base = ''.join(f.readlines()).strip().split('\n')
#     proxies = {}
#     for proxy in proxy_base:
#         proxies['http'] = f'http://{proxy}',
#         proxies['https'] = f'https://{proxy}'
#         print(proxies)


def get_page(url):
    req = requests.get(url, headers=headers)
    src = req.text

    with open('index.html', 'w') as file:
        index = file.write(src)
    return index


def get_page_data(url):
    # with open('buldoors.csv', 'w', encoding='UTF-8') as file:
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

    product_urls = []
    # articles = []
    req = requests.get(url, headers=headers, timeout=3)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    pages = int(soup.find('nav', class_='woocommerce-pagination').find_all('a')[-2].text)
    time.sleep(1)
    # create pagination
    for page in range(1, 2):  # pages + 1
        page_url = f'https://buldoors-moscow.ru/product-category/doors-buldoors/page/{page}/'
        req = requests.get(page_url, headers=headers)
        res = req.text
        soup = BeautifulSoup(res, 'lxml')

        # get item urls from current site
        for urls in soup.find_all('a', class_='woocommerce-LoopProduct-link woocommerce-loop-product__link'):
            items_url = urls.get('href')

            # get item info

        #     req = requests.get(items_url, headers=headers)
        #     res = req.text
        #     soup = BeautifulSoup(res, 'lxml')
        #     name = soup.find('h1', class_='product_title entry-title').text
        #     price = soup.find('div', class_='product__price').text.replace('₽', '').strip()
        #     img_1 = domain + soup.find('div', class_='product__img-wrap').find('img').get('src')
        #     img_2 = domain + soup.find('div', class_='product__img-wrap').find('img').find_next('img').get('src')
        #     img = (img_1, img_2)
        #     try:
        #         desc_1 = soup.find('div', class_='product__property-name', text=re.compile('Описание')).find_next(
        #             'div', class_='product__property-value')
        #         desc_2 = soup.find('div', class_='product__property-name',
        #                            text=re.compile('Особенности')).find_next('div', class_='product__property-value')
        #         desc_3 = soup.find('div', class_='product__property-name', text=re.compile('Качество')).find_next(
        #             'div', class_='product__property-value')
        #         description = desc_1 + desc_2 + desc_3
        #     except:
        #         description = None
        #     try:
        #         metal_thickness = soup.find('div', class_='product__property-name',
        #                                     text=re.compile('Толщина стали')).find_next('div',
        #                                                                                 class_='product__property-value').text
        #     except:
        #         metal_thickness = None
        #     try:
        #         seal_contours = soup.find('div', class_='product__property-name',
        #                                   text=re.compile('Уплотнение')).find_next('div',
        #                                                                            class_='product__property-value').text
        #     except:
        #         seal_contours = None
        #     try:
        #         size = soup.find('div', class_='product__property-name', text=re.compile('Размер')).find_next('div',
        #                                                                                                       class_='product__property-value').text
        #     except:
        #         size = None
        #     try:
        #         door_filling = soup.find('div', class_='product__property-name',
        #                                  text=re.compile('Утепление')).find_next('div',
        #                                                                          class_='product__property-value').text
        #     except:
        #         door_filling = None
        #     try:
        #         external_panel = soup.find('div', class_='product__property-name',
        #                                    text=re.compile('Отделка снаружи')).find_next('div',
        #                                                                                  class_='product__property-value').text
        #     except:
        #         external_panel = None
        #     img_external_panel = img_1
        #     try:
        #         internal_panel = soup.find('div', class_='product__property-name',
        #                                    text=re.compile('Отделка внутри')).find_next('div',
        #                                                                                 class_='product__property-value').text
        #     except:
        #         internal_panel = None
        #     img_internal_panel = img_2
        #     glazed_window = ['Да' if 'стекло' in internal_panel else 'Нет']
        #     mirror = ['Да' if 'зеркало' in internal_panel else 'Нет']
        #     thermal_break = ['Да' if 'терморазрыв' in internal_panel else 'Нет']
        #     magnetic_seal = ['Да' if 'магнит' in internal_panel else 'Нет']
        #     external_panel_ = ['Да' if external_panel is not None else 'Нет']
        #     time.sleep(1)
        #
        #     with open('buldoors.csv', 'a', encoding='UTF-8') as file:
        #         writer = csv.writer(file)
        #         writer.writerow(
        #             (
        #                 name,
        #                 price,
        #                 img,
        #                 description,
        #                 external_panel_,
        #                 'Бульдорс',
        #                 img_external_panel,
        #                 external_panel,
        #                 img_internal_panel,
        #                 internal_panel,
        #                 metal_thickness,
        #                 seal_contours,
        #                 size,
        #                 door_filling,
        #                 glazed_window,
        #                 mirror,
        #                 thermal_break,
        #                 magnetic_seal,
        #                 None,
        #             )
        #         )


def main():
    # get_page(site)
    get_page_data(site)


if __name__ == '__main__':
    main()
