import csv
import re
import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent  # pip install fake-useragent

ua = UserAgent()

site = 'https://www.dveriregionov.ru/catalog/metallicheskie_dveri/'
domain = 'https://www.dveriregionov.ru'

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
    with open('dveriregionov.csv', 'w', encoding='UTF-8') as file:
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
    # product_urls = []
    # articles = []
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    pages = int(soup.find('div', id='newpagenna').find_all('span')[-2].text)

    for page in range(1, 2):  # pages + 1
        page_url = f'https://www.dveriregionov.ru/catalog/metallicheskie_dveri/?PAGEN_1={page}'
        req = requests.get(page_url, headers=headers)
        res = req.text
        soup = BeautifulSoup(res, 'lxml')

        for urls in soup.find_all('a', class_='itemlink'):
            items_url = domain + urls.get('href')
            # product_urls.append(items_url)
            req = requests.get(items_url, headers=headers)
            res = req.text
            soup = BeautifulSoup(res, 'lxml')

            for panel in soup.find_all('a', class_='changepicture'):
                panel_url = domain + panel.get('href')
                req = requests.get(panel_url, headers=headers)
                res = req.text
                soup = BeautifulSoup(res, 'lxml')

                name = soup.find('h1', class_='title-h1').text.strip()
                img_1 = domain + soup.find('img', id='dooroutpicture').get('src')
                img_2 = domain + soup.find('img', id='doorinpicture').get('src')
                image = (img_1, img_2)
                try:
                    gallery = [domain + img.get('href') for img in soup.find('div', class_='add-photo').find_all('a')]
                except:
                    gallery = None
                try:
                    desc = soup.find('ul', class_='uk-switcher')
                except:
                    desc = None
                price = soup.find('div', id='itogpricedoors').text.strip()
                manufacturer = soup.find('td', text=re.compile('Производитель')).next_sibling.text
                size = soup.find('td', text=re.compile('Размер')).next_sibling.text
                metal_thickness = soup.find('td', text=re.compile('Толщина листа')).next_sibling.text
                door_filling = soup.find('td', text=re.compile('Утеплитель')).next_sibling.text
                thermal_break = soup.find('td', text=re.compile('Терморазрыв')).next_sibling.text
                mirror = ['Да' if 'зеркало' in name else 'Нет']
                img_internal_panel = img_2
                img_external_panel = img_1
                internal_panel = soup.find('span', class_='value nameinnerpanel').text.strip()
                external_panel = soup.find('span', class_='value nameouterpanel').text.strip()
                external_panel_ = ['Да' if external_panel is not None else 'Нет']

                with open('dveriregionov.csv', 'a', encoding='UTF-8') as file:
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
                            external_panel,
                            img_internal_panel,
                            internal_panel,
                            metal_thickness,
                            None,
                            size,
                            door_filling,
                            None,
                            mirror,
                            thermal_break,
                            None,
                            gallery,
                            )
                        )


def main():
    # get_page(site)
    get_page_data(site)


if __name__ == '__main__':
    main()