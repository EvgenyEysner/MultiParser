import csv
import re
import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent  # pip install fake-useragent
from selenium import webdriver
from selenium.webdriver.common.by import By

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
        # get_items_data(page_url)


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
    # with open('argus.csv', 'w', encoding='UTF-8') as file:
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
    with open(page) as f:
        src = f.read()
        soup = BeautifulSoup(src, 'lxml')

        pages = int(soup.find('ul', class_='pager').find_all('a')[-1].get('href').split('=')[2].strip())
        for page in range(0, 1): # pages + 1
            page_url = f'https://argusmsk.ru/category/all?sort_by=totalcount&page={page}'
            soup = make_request(page_url)
            links = [domain + link.find('a').get('href') for link in soup.find_all('div', class_='door')]
        for item in links:
            soup = make_request(item)
            try:
                panels = soup.find('div', class_='item-desc').find_all(href=re.compile('paneli'))
                desc = soup.find('div', id='block-system-main')
                name = soup.find('div', id=re.compile('node-')).find('h2').text.replace('✓ Хит продаж', '').replace('✓ Скидки и Акции', '')
                out_price = soup.find(text=re.compile('Снаружи металл')).next.text.replace('₽', '').strip()
                in_price = soup.find(text=re.compile('Снаружи панель')).next.text.replace('₽', '').strip()
            except:
                out_price = None
                in_price = None
            print(in_price)
            
            # for item in links:
            #     browser.get(item)
            #     try:
            #         name = browser.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div[2]/div/div/div[1]/h2').text.split('\n')[0]
            #     except:
            #         name = None
            #     try:
            #         desc = browser.find_element(By.CLASS_NAME, 'item-desc').text.strip()
            #     except:
            #         desc = None
            #     try:
            #         price = browser.find_element(By.CSS_SELECTOR,'.ci-price > center:nth-child(1)').text.replace('₽', '')
            #
            #     except:
            #         # price = None
            #         price_out = browser.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div[2]/div/div/div[1]/div[2]//*[contains(text(),"Снаружи металл")]//following-sibling::span').text
            #         price_in = browser.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div[2]/div/div/div[1]/div[2]//*[contains(text(),"Снаружи панель")]//following-sibling::span').text
            #     # except:
            #     #     price_out = None
            #     #     price_in = None
            #         print(price_in)




def get_items_data(page_url):
    pass


def main():
    # get_page(site)
    get_page_data('index.html')


if __name__ == '__main__':
    main()