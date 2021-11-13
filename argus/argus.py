import csv
import re
import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent  # pip install fake-useragent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# options = webdriver.FirefoxOptions()
# options.set_preference('dom.webdriver.enabled', False)
ua = UserAgent()
# options.add_argument(ua.random)
# options.add_argument('--headless')
# browser = webdriver.Firefox(executable_path='/home/evgeny/PycharmProjects/MultiParser/geckodriver', options=options)
site = 'https://argusmsk.ru/category/all?sort_by=totalcount'
domain = 'https://argusmsk.ru'

headers = {
    'User-Agent': ua.random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
}


def pagination(pages):

    for page in range(1, pages + 1):
        page_url = f'https://argusmsk.ru/category/all?sort_by=totalcount&page={page}'
        return page_url


def make_request(url):
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    return soup


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
        with open('argus.csv', 'w', encoding='UTF-8') as file:
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
        pages = int(soup.find('ul', class_='pager').find_all('a')[-1].get('href').split('=')[2].strip())
        for page in range(0, pages + 1):  # pages + 1
            page_url = f'https://argusmsk.ru/category/all?sort_by=totalcount&page={page}'
            soup = make_request(page_url)
            urls = [domain + link.find('a').get('href') for link in soup.find_all('div', class_='door')]
            for url in urls:
                soup = make_request(url)
                try:
                    desc = soup.find_all('div', class_='item-desc')
                except:
                    desc = None
                try:
                    name = soup.find('small').find_all_previous()[1].text.replace('✓', '').replace('Скидки и Акции', '').replace('Хит продаж', '').upper()
                except:
                    name = None
                try:
                    price = soup.find('div', class_='ci-price').text.replace('₽', '')
                except:
                    price = None
                try:
                    price_1 = soup.find('div', class_='item-desc').find(text=re.compile(r'\d{2}')).replace('₽', '').replace('.', ' ').strip()
                except:
                    price_1 = None
                try:
                    construction = soup.find(text=re.compile('конструкция', re.IGNORECASE)).next_element.next_element
                except:
                    construction = None
                try:
                    metal_thickness = construction.split('.')[1].split(',')[0]
                except:
                    metal_thickness = None
                try:
                    seal_contours = construction.split('.')[4]
                except:
                    seal_contours = None
                try:
                    thermal_break = ['Да' if 'терморазрыв' in construction else 'Нет']
                except:
                    thermal_break = None
                try:
                    magnetic_seal = ['Да' if 'магнит' in construction else 'Нет']
                except:
                    magnetic_seal = None
                try:
                    mirror = ['Да' if 'зеркало' in name else 'Нет']
                except:
                    mirror = None
                try:
                    glazed_window = ['Да' if 'стекло' in construction else 'Нет']
                except:
                    glazed_window = None
                try:
                    size = soup.find(text=re.compile('Размеры', re.IGNORECASE)).find_all_previous('span')[1].text.split(':')[1]
                except:
                    size = None
                try:
                    door_filling = soup.find(text=re.compile('Утеплитель', re.IGNORECASE)).find_all_previous('span')[1].text.split(':')[1]
                except:
                    door_filling = None
                manufacturer = 'АРГУС'
                gallery = None
                # try:
                #     ext_panel_links = [url.get('href') for url in soup.find_all('a', href=re.compile('vneshnie'))]
                #     external_panel_ = ['Да' if ext_panel_links else 'Нет']
                #     for link in ext_panel_links:
                #         soup = make_request(link)
                #         e_panel = soup.find('div', class_='media-body').find_all(text=re.compile('Цвет'))
                #     external_panel = [panel.find_all_previous('span')[1].text.split(':')[1].replace('.', '') for panel in e_panel]
                #     img_external_panel = [panel.find_previous('a', class_='colorbox').get('href') for panel in e_panel]
                    #     e_panel = soup.find('div', class_='media-body').find_all(text=re.compile('Цвет'))
                    # for panel in e_panel:
                    #     external_panel = panel.find_all_previous('span')[1].text.split(':')[1].replace('.', '')
                    #     img_external_panel = panel.find_previous('a', class_='colorbox').get('href')
                # except:
                #     external_panel = None
                #     img_external_panel = None
                try:
                    image = soup.find('img', attrs={'width': '500'}).get('src')
                except:
                    None
                try:
                    ext_panel_links = [url.get('href') for url in soup.find_all('a', href=re.compile('vneshnie'))]
                    external_panel = soup.find(text=re.compile('ВНЕШНЯЯ ОТДЕЛКА', re.IGNORECASE)).find_all_previous('span')[1].text.split(':')[1]
                    external_panel_ = ['Да' if ext_panel_links else 'Нет']
                    img_external_panel = image
                except:
                    external_panel = None
                    img_external_panel = None
                # try:
                #     int_panel_links = [url.get('href') for url in soup.find_all('a', href=re.compile('vnutrennie'))]
                #     for int_panel in int_panel_links:
                #         soup = make_request(int_panel)
                #         i_panels = soup.find_all(text=re.compile('Возможные цвета'))
                #     internal_panel = [internal.find_previous('td').text.split(':')[1].replace('\n\t\t\t', '').replace('----', '') for internal in i_panels]
                #     img_internal_panel = [internal.find_previous('a', class_='colorbox').get('href') for internal in i_panels]
                #     # for internal in i_panels:
                #     #     internal_panel = internal.find_previous('td').text.split(':')[1].replace('\n\t\t\t', '').replace('----', '')
                #     #     img_internal_panel = internal.find_previous('a', class_='colorbox').get('href')
                # except:
                #     img_internal_panel = None
                #     internal_panel = None
                try:
                    int_panel_links = [url.get('href') for url in soup.find_all('a', href=re.compile('vnutrennie'))]
                    internal_panel = soup.find(text=re.compile('ВНУТРЕННЯЯ ОТДЕЛКА', re.IGNORECASE)).find_all_previous('span')[1].text.split(':')[1]
                    img_internal_panel = image
                except:
                    internal_panel = None
                    img_internal_panel = None
                with open('argus.csv', 'a', encoding='UTF-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(
                        (
                            name,
                            price or price_1,
                            image,
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
    # get_page(site)
    get_page_data('index.html')


if __name__ == '__main__':
    main()