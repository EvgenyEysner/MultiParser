import csv
import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent  # pip install fake-useragent
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.FirefoxOptions()
options.set_preference('dom.webdriver.enabled', False)
ua = UserAgent()
options.add_argument(ua.random)
options.add_argument('--headless')
browser = webdriver.Firefox(executable_path='/home/evgeny/PycharmProjects/MultiParser/geckodriver', options=options)
site = 'https://labirintdoors.ru'

headers = {
    'User-Agent': ua.random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
}


def make_request(url):
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    return soup


def pagination(pages, url):

    for page in range(1, pages + 1):
        page_url = f'{url}/?sort=position&direction=asc&page={page}'
        get_items_data(page_url)


def get_page(url):
    req = requests.get(url, headers=headers)
    src = req.text

    with open('index.html', 'w') as file:
        index = file.write(src)
    return index


def get_page_data(page):
    with open('labirint.csv', 'w', encoding='UTF-8') as file:
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
    with open(page) as f:
        src = f.read()
        soup = BeautifulSoup(src, 'lxml')

        try:
            for urls in soup.find('div', class_='product-sections-01__inner section__content').find_all('a', class_='product-sections-01-item__img-container'):
                url = site + urls.get('href')
                soup = make_request(url)
                pages = int(soup.find('ul', class_='products-pagination__list').find_all('a')[-2].text)
                pagination(pages, url)
        except:
            for links in soup.find('ul', class_='sections-01-list sections-01-list_columns_four sections-01__list').find_all('a'):
                link = site + links.get('href')
                soup = make_request(link)
                pages = int(soup.find('ul', class_='products-pagination__list').find_all('a')[-2].text)
                pagination(pages, url)


def get_items_data(url):

    browser.get(url)
    links = browser.find_elements(By.CLASS_NAME, 'products-list-01-item__header')
    item_urls = [link.find_element_by_tag_name('a').get_attribute('href') for link in links]
    for item in item_urls:
        browser.get(item)
        time.sleep(2)

        name = browser.find_element(By.CLASS_NAME, 'product-01__title').text.strip()
        price = browser.find_element(By.CLASS_NAME, 'product-01__price').text.split()[0]
        desc = browser.find_element(By.CLASS_NAME, 'product-01__parameters-container').text
        image = browser.find_element(By.XPATH,
                                     '/html/body/div[2]/main/div[2]/div/div/div/div/div[1]/div/div/div/a').get_attribute(
            'href')
        try:
            gallery = [img.get_attribute('href') for img in browser.find_elements(By.XPATH,
                                                                                  '/html/body/div[2]/main/div[2]/div/div/div/div/div[1]/div/div[2]/div[1]/a')]
        except:
            gallery = None
        try:
            metal_thickness = browser.find_element(By.XPATH,
                                                   '/html/body/div[2]/main/div[2]/div/div/div/div/div[3]/div/div/div[5]//*[contains(text(),"Конструкция")]//following-sibling::dd').text
        except:
            metal_thickness = None
        try:
            seal_contours = browser.find_element(By.XPATH,
                                                 '/html/body/div[2]/main/div[2]/div/div/div/div/div[3]/div/div/div[5]//*[contains(text(),"Контур")]//following-sibling::dd').text
        except:
            seal_contours = None
        try:
            door_filling = browser.find_element(By.XPATH,
                                                '/html/body/div[2]/main/div[2]/div/div/div/div/div[3]/div/div/div[5]//*[contains(text(),"Утепление")]//following-sibling::dd').text
        except:
            door_filling = None
        try:
            external_panel = browser.find_element(By.XPATH,
                                                  '/html/body/div[2]/main/div[2]/div/div/div/div/div[3]/div/div/div[5]//*[contains(text(),"Отделка снаружи")]//following-sibling::dd').text
        except:
            external_panel = None
        external_panel_ = ['Да' if 'панель' in external_panel else 'Нет']
        try:
            internal_panel = browser.find_element(By.XPATH,
                                                  '/html/body/div[2]/main/div[2]/div/div/div/div/div[3]/div/div/div[5]//*[contains(text(),"Внутренняя отделка")]//following-sibling::dd').text
        except:
            internal_panel = None
        try:
            thermal_break = browser.find_element(By.XPATH,
                                                 '/html/body/div[2]/main/div[2]/div/div/div/div/div[3]/div/div/div[5]//*[contains(text(),"Терморазрыв")]//following-sibling::dd').text
        except:
            thermal_break = None
        img_external_panel = image
        img_internal_panel = image
        try:
            magnetic_seal = ['Да' if 'магнит' in seal_contours else 'Нет']
        except:
            magnetic_seal = None
        try:
            mirror = ['Да' if 'зеркало' in internal_panel else 'Нет']
        except:
            mirror = None
        try:
            glazed_window = ['Да' if 'стекло' in internal_panel else 'Нет']
        except:
            glazed_window = None
        size = None

        with open('labirint.csv', 'a', encoding='UTF-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    name,
                    price,
                    image,
                    desc,
                    external_panel_,
                    'Лабиринт',
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
