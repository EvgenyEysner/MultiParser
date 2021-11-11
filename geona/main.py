import csv
import re
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()

site = 'https://geona-russia.ru/vhodnye-dveri?'
domain = 'https://geona-russia.ru/'

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


def get_data(url):
    with open('geona.csv', 'w', encoding='UTF-8') as file:
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

    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    pages = int(soup.find('ul', class_='pagination').find_all('a')[-3].text)

    for page in range(1, pages + 1):
        page_url = f'https://geona-russia.ru/vhodnye-dveri?page={page}'
        req = requests.get(page_url, headers=headers)
        res = req.text
        soup = BeautifulSoup(res, 'lxml')
        for urls in soup.find_all('div', class_='product-thumb'):
            items_url = urls.find('a').get('href')
            req = requests.get(items_url, headers=headers)
            res = req.text
            soup = BeautifulSoup(res, 'lxml')

            name = soup.find('h1', attrs={'itemprop': 'name'}).text.strip()
            price = soup.find('div', id='price').find_next('span').text
            img = [image.get('href') for image in soup.find_all('a', class_='thumbnail')]
            try:
                desc = soup.find('div', id='tab-description')
            except:
                desc = None

            manufacturer = 'Фабрика GEONA'
            img_external_panel = img[0]
            img_internal_panel = img[1]
            try:
                door_filling = soup.find(text=re.compile('Утепление полотна')).next_element.text
            except:
                door_filling = None
            gallery = None
            try:
                external_panel = soup.find(text=re.compile('наружная')).split(' ')[4].text
            except:
                external_panel = None
            try:
                internal_panel = soup.find(text=re.compile('внутренняя')).replace('-', '').replace('Декоративные панели: ', '').strip()
            except:
                internal_panel = None
            try:
                external_panel_ = ['Да' if 'наружная' in soup.find(text=re.compile('наружная')) else 'Нет']
            except:
                external_panel_ = None
            try:
             seal_contours = soup.find('td', text=re.compile('Контуры уплотнителя')).find_next_sibling('td').text.strip()
            except:
                seal_contours = None
            try:
                size = soup.find('td', text=re.compile('Размер кованного элемента')).find_next_sibling('td').text.strip()
            except:
                size = None
            try:
                metal_thickness = soup.find('td', text=re.compile('Толщина металла')).find_next_sibling('td').text.strip()
                metal_thickness_1 = soup.find('p', text=re.compile('Толщина металла'))
            except:
                metal_thickness = None
            try:
                thermal_break = ['Да' if 'терморазрыв' in soup.find('div', id='tab-specification').text else 'Нет']
            except:
                thermal_break = None
            try:
                glazed_window = ['Да' if 'стекло' in name else 'Нет']
            except:
                glazed_window = None
            try:
                mirror = ['Да' if 'зеркало' in soup.find('div', id='tab-specification').text else 'Нет']
            except:
                mirror = None
            try:
                magnetic_seal = ['Да' if 'магнит' in seal_contours else 'Нет']
            except:
                magnetic_seal = None

            with open('geona.csv', 'a', encoding='UTF-8') as file:
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
                        [metal_thickness or metal_thickness_1],
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
    get_data(site)
    get_page(site)


if __name__ == '__main__':
    main()