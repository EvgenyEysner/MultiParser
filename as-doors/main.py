import csv
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re

ua = UserAgent()
ua = UserAgent()

site = 'https://as-doors.ru/onstock'
domain = 'https://as-doors.ru/'
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


def get_items_urls(page):
    item_urls = []
    items = []
    with open('asdoors.csv', 'w', encoding='UTF-8') as file:
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
    # get item urls
    with open(page) as f:
        src = f.read()
        soup = BeautifulSoup(src, 'lxml')

        for urls in soup.find_all('div', class_='item4'):
            url = domain + urls.find('a').get('href')
            item_urls.append(url)

            # get item page
            req = requests.get(url, headers=headers)
            src = req.text
            soup = BeautifulSoup(src, 'lxml')

            name = soup.find('h1').text.replace('«', '').replace('»', '')
            img_out = domain + soup.find('div', class_='thumb').find('img').get('src')
            img_in = domain + soup.find('div', id='tab1').find('img').get('src')
            external_panel = soup.find('div', class_='table').find_all('p')[3].find('span').text
            external_panel_ = ['Нет' if 'металл' in external_panel else 'Да']
            internal_panel = soup.find('div', class_='table').find_all('p')[4].find('span').text
            desc = soup.find_all('div', class_='txt')[1]
            price = soup.find('div', class_='price').text.replace('Цена:', '').strip()
            size = soup.find('div', class_='table').find_all('p')[10].find('span').text.replace(';', '/').strip()
            door_filling = soup.find('div', class_='table').find_all('p')[9].find('span').text.replace('«', '').replace(
                '»', '')
            metal_thickness = soup.find('div', class_='table').find_all('p')[3].find('span').text.split('мм')[0].strip()
            seal_contours = soup.find(text=re.compile('Дверная коробка')).find_next('span').text.strip()
            gallery = domain + soup.find('div', class_='gallery').find('img').get('src')
            glazed_window = ['Да' if 'стекло' in internal_panel else 'Нет']
            mirror = ['Да' if 'зеркало' in name else 'Нет']
            thermal_break = ['Да' if 'терморазрыв' in seal_contours else 'Нет']

            items.append(
                {
                    'Наименование': name,
                    'Панель внешняя': external_panel,
                    'Картинка панель внешняя': img_out,
                    'Панель внутренняя': internal_panel,
                    'Картинка панель внутренняя': img_in,
                    'Описание товара': desc,
                    'Цена товара': price,
                    'Изображение товара': (img_out, img_in),
                    'Размеры': size,
                    'Производитель(Фирма производитель)': 'Общество с ограниченной ответственностью «АСД»',
                    'Контуры уплотнения': None,
                    'Наполнение двери': door_filling,
                    'Толщина метала/ мм': metal_thickness,
                    'Магнитный уплотнитель(да\нет)': None,
                    'Зеркало(да\нет)': ['Да' if 'зеркало' in name else 'Нет'],
                    'Терморазрыв(да\нет)': None,
                    'Внешняя панель(да\нет)': None,
                    'Стеклопакет(да\нет)': None,
                    'Галерея': gallery
                }
            )
            with open('asdoors.csv', 'a', encoding='UTF-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        name,
                        price,
                        (img_in, img_out),
                        desc,
                        external_panel_,
                        'Общество с ограниченной ответственностью «АСД»',
                        img_out,
                        external_panel,
                        img_in,
                        internal_panel,
                        metal_thickness,
                        seal_contours,
                        size,
                        door_filling,
                        glazed_window,
                        mirror,
                        thermal_break,
                        None,
                        gallery,
                    )
                )


def main():
    get_page(site)
    get_items_urls('index.html')


if __name__ == '__main__':
    main()
