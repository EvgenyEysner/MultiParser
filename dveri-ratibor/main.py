import csv
import re

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent  # pip install fake-useragent

ua = UserAgent()

site = 'https://dveri-ratibor.ru/magazin/folder/katalog-dveri'
domain = 'https://dveri-ratibor.ru'

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

    with open(page) as f:
        src = f.read()
        soup = BeautifulSoup(src, 'lxml')
        with open('ratibor.csv', 'w', encoding='UTF-8') as file:
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
        for urls in soup.find_all('div', class_='product-name'):
            url = domain + urls.find('a').get('href')

            req = requests.get(url, headers=headers)
            src = req.text
            soup = BeautifulSoup(src, 'lxml')

            name = soup.find('h1', class_='h1').text.strip()
            images = soup.find('div', class_='product-image').find_all('img')
            image = domain + images[0].get('src')
            img_external_panel = domain + images[1].get('src')
            img_internal_panel = domain + images[2].get('src')
            price = soup.find('div', class_='price-current').find('strong').text.strip()
            gallery = (image, img_internal_panel, img_external_panel)
            manufacturer = soup.find('div', class_='option-title', text=re.compile('Производитель')).next_sibling.text
            external_panel = soup.find('div', class_='option-title', text=re.compile('Покрытие снаружи')).next_sibling.text
            internal_panel = soup.find('div', class_='option-title', text=re.compile('Покрытие внутри')).next_sibling.text
            size = soup.find('div', class_='option-title', text=re.compile('Размеры')).next_sibling.text
            seal_contours = soup.find('th', text=re.compile('Контуры уплотнения')).next_sibling.text
            metal_thickness = soup.find('th', text=re.compile('Конструкция')).next_sibling.text
            door_filling = soup.find('th', text=re.compile('Утепление')).next_sibling.text
            mirror = ['Да' if 'зеркало' in internal_panel else 'Нет']
            thermal_break = ['Да' if 'терморазрыв' in soup.find('th', text=re.compile('наполнение двери')).next_sibling.text else 'Нет']
            magnetic_seal = None
            glazed_window = None
            try:
                desc = soup.find('div', class_='param-body param_text')
            except:
                desc = None

            with open('ratibor.csv', 'a', encoding='UTF-8') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        name,
                        price,
                        image,
                        desc,
                        None,
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
    get_page_data('index.html')


if __name__ == '__main__':
    main()