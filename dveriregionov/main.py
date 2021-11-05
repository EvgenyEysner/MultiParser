import csv
import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent  # pip install fake-useragent
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.FirefoxOptions()
ua = UserAgent()
options.add_argument(ua.random)
options.set_preference('dom.webdriver.enabled', False)
options.add_argument('--headless')

browser = webdriver.Firefox(executable_path='/home/evgeny/PycharmProjects/MultiParser/geckodriver', options=options)

site = 'https://www.dveriregionov.ru/catalog/metallicheskie_dveri/'
domain = 'https://www.dveriregionov.ru'

headers = {
    'User-Agent': ua.random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
}


def make_request(url):
    req = requests.get(url, headers=headers)
    res = req.text
    soup = BeautifulSoup(res, 'lxml')
    return soup


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
    soup = make_request(url)
    pages = int(soup.find('div', id='newpagenna').find_all('span')[-2].text)

    for page in range(1, pages + 1):  # pages + 1 start page with pagination
        page_url = f'https://www.dveriregionov.ru/catalog/metallicheskie_dveri/?PAGEN_1={page}'
        soup = make_request(page_url)
        print(f'обработана страница: {page}')

        for urls in soup.find_all('a', class_='itemlink'):  # all items page
            items_urls = domain + urls.get('href')
            browser.get(items_urls)

            panels = browser.find_elements(By.CLASS_NAME, 'changepicture')
            color_links = [link.get_attribute('href') for link in panels]
            time.sleep(2)
            for link in color_links:
                browser.get(link)
                picture_block = browser.find_elements(By.CSS_SELECTOR, 'div.detail-small-tabs:nth-child(5) > ul:nth-child(2) > li:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)')
                picture_links = [link.get_attribute('href') for link in picture_block]
                time.sleep(1)

                for picture in picture_links:
                    browser.get(picture)
                    try:
                        img_1 = browser.find_element(By.ID, 'dooroutpicture').get_attribute('src')
                        img_2 = browser.find_element(By.ID, 'doorinpicture').get_attribute('src')
                        image = (img_1, img_2)
                    except:
                        image = None
                    try:
                        gallery = [link.find_element(By.TAG_NAME, 'a').get_attribute('href') for link in browser.find_elements(By.CLASS_NAME, 'slide')]
                    except:
                        gallery = None
                    try:
                        name = browser.find_element(By.CLASS_NAME, 'title-h1').text.strip()
                    except:
                        name = None
                    try:
                        desc = browser.find_element(By.ID, 'propperties').text
                    except:
                        desc = None
                    try:
                        price = browser.find_element(By.ID, 'itogpricedoors').text.split()[0]
                    except:
                        price = None
                    try:
                        manufacturer = browser.find_element(By.CSS_SELECTOR, '#propperties > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)').text
                    except:
                        manufacturer = None
                    try:
                        size = browser.find_element(By.CSS_SELECTOR, '#propperties > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2)').text
                    except:
                        size = None
                    try:
                        metal_thickness = browser.find_element(By.CSS_SELECTOR, '#propperties > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(5) > td:nth-child(2)').text
                    except:
                        metal_thickness = None
                    try:
                        door_filling = browser.find_element(By.CSS_SELECTOR, '#propperties > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(15) > td:nth-child(2)').text
                    except:
                        door_filling = None
                    try:
                        thermal_break = browser.find_element(By.CSS_SELECTOR, '#propperties > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(18) > td:nth-child(2)').text
                    except:
                        thermal_break = None
                    try:
                        internal_panel = browser.find_element(By.XPATH, '/html/body/section/div[1]/div/div[2]/div[2]/div[1]/div[2]/div/div[1]/div[1]/div[1]/div[2]/div[2]/div[3]/span').text
                    except:
                        internal_panel = None
                    try:
                        external_panel = browser.find_element(By.XPATH, '/html/body/section/div[1]/div/div[2]/div[2]/div[1]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div[2]/div[3]/span').text
                    except:
                        external_panel = None
                    mirror = ['Да' if 'зеркало' in name else 'Нет']
                    img_internal_panel = img_2
                    img_external_panel = img_1
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