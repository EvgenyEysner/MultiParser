import csv
import re
import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent  # pip install fake-useragent
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.FirefoxOptions()
options.set_preference('dom.webdriver.enabled', False)
browser = webdriver.Firefox(executable_path='/home/evgeny/PycharmProjects/MultiParser/geckodriver', options=options) # add Selenium

user = UserAgent().random

site = 'https://buldoors-moscow.ru/product-category/doors-buldoors/'
domain = 'https://buldoors-moscow.ru'

headers = {
    'User-Agent': user,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
}


def get_page(url):
    req = requests.get(url, headers=headers)
    src = req.text

    with open('index.html', 'w') as file:
        index = file.write(src)
    return index


def get_page_data(url):
    with open('buldoors.csv', 'w', encoding='UTF-8') as file:
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
    pages = int(soup.find('nav', class_='woocommerce-pagination').find_all('a')[-2].text)
    time.sleep(1)
    # create pagination
    for page in range(1, pages + 1):  # pages + 1
        page_url = f'https://buldoors-moscow.ru/product-category/doors-buldoors/page/{page}/'
        browser.get(page_url)
        print(page_url)
        time.sleep(2)

        req = requests.get(page_url, headers=headers)
        res = req.text
        soup = BeautifulSoup(res, 'lxml')

        # get item urls from current site
        for urls in soup.find_all('a', class_='woocommerce-LoopProduct-link woocommerce-loop-product__link'):
            items_url = urls.get('href')
            browser.get(items_url)
            time.sleep(3)

            # get item info
            name = browser.find_element_by_xpath('/html/body/div[1]/div[4]/div/div[2]/main/div[2]/div[2]/h1').text
            price = browser.find_element_by_xpath('/html/body/div[1]/div[4]/div/div[2]/main/div[2]/div[2]/p/span').text.replace('₽', '').strip()
            desc = browser.find_element_by_xpath('//*[@id="tab-description"]').text.replace('Описание', '').strip()
            try:
                image = browser.find_element(By.CLASS_NAME, 'woocommerce-product-gallery__image').find_element_by_tag_name('a').get_attribute('href')
            except:
                image = None
            metal = browser.find_element_by_xpath('/html/body/div[1]/div[4]/div/div[2]/main/div[2]/div[3]/div[1]/p[2]').text
            metal_thickness = re.findall(r"(?<![a-zA-Z:])[-+]?\d*\.?\d+", metal)[1] + 'мм'  # get float int from string, +\d == int
            seal_contours = browser.find_element_by_xpath('/html/body/div[1]/div[4]/div/div[2]/main/div[2]/div[3]/div[1]/p[5]').text.replace('Уплотнитель', '').split('.')[0].strip()
            size = browser.find_element_by_xpath('/html/body/div[1]/div[4]/div/div[2]/main/div[2]/div[3]/div[1]/p[1]').text.replace('Размер', '').strip()
            door_filling = browser.find_element_by_xpath('/html/body/div[1]/div[4]/div/div[2]/main/div[2]/div[3]/div[1]/p[3]').text.replace('Утепление полотна', '').split(':')[0].strip()
            browser.find_element_by_xpath('/html/body/div[1]/div[4]/div/div[2]/main/div[2]/div[3]/ul/li[2]/a').click()
            time.sleep(1)
            external_panel = browser.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div[2]/main/div[2]/div[3]/div[2]/table/tbody/tr[5]/td/p').text.strip()
            internal_panel = browser.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div[2]/main/div[2]/div[3]/div[2]/table/tbody/tr[6]/td/p').text.strip()
            external_panel_ = ['Нет' if 'Металл' in external_panel else 'Да']
            manufacturer = browser.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div[2]/main/div[2]/div[3]/div[2]/table/tbody/tr[4]/td/p').text.strip()
            try:
                mirror = ['Да' if 'зеркало' in browser.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div[2]/main/div[2]/div[3]/div[2]/table/tbody/tr[7]/td/p').text else 'Нет']
            except:
                mirror = None
            try:
                glazed_window = ['Да' if 'стекло' in browser.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div[2]/main/div[2]/div[3]/div[2]/table/tbody/tr[7]/td/p').text else 'Нет']
            except:
                glazed_window = None
            try:
                gallery = browser.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div[2]/main/div[2]/div[1]/div[2]/figure/div[2]/a').get_attribute('href')
            except:
                gallery = None

            img_external_panel = image
            img_internal_panel = image
            thermal_break = ['Да' if 'терморазрыв' in internal_panel else 'Нет']
            magnetic_seal = ['Да' if 'магнит' in internal_panel else 'Нет']
            time.sleep(2)

            with open('buldoors.csv', 'a', encoding='UTF-8') as file:
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
    get_page_data(site)


if __name__ == '__main__':
    main()