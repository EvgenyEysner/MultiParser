import csv
import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent  # pip install fake-useragent
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.FirefoxOptions()
browser = webdriver.Firefox(executable_path='/home/evgeny/PycharmProjects/MultiParser/geckodriver', options=options)
ua = UserAgent()
options.add_argument(ua.random)
options.set_preference('dom.webdriver.enabled', False)
options.add_argument('--headless')

site = 'https://intecron-msk.ru/mezhkomnatnie-dveri/v-nalichii.html'
domain = 'https://intecron-msk.ru'

headers = {
    'User-Agent': ua.random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
}


def get_page(url):
    req = requests.get(url, headers=headers)
    src = req.text

    with open('index_2.html', 'w') as file:
        index = file.write(src)
    return index


def get_page_data(page):
    with open(page) as f:
        src = f.read()
        soup = BeautifulSoup(src, 'lxml')
        with open('intecron_2.csv', 'w', encoding='UTF-8') as file:
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
        for urls in soup.find_all('div', class_='catalog-item__title'):
            url = urls.find('a').get('href')
            browser.get(url)
            time.sleep(2)

            name = browser.find_element(By.TAG_NAME, 'h1').text
            desc = browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div/div/div[2]/div[3]/div[2]').text
            image = browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/div/div[1]/a').get_attribute('href')
            gallery = None
            try:
                metal_thickness = browser.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div[1]/div/div/div[2]/div[3]/div[2]/div[1]/div/div[1]/div[2]/p[2]').text.strip()
            except:
                metal_thickness = None
            try:
                seal_contours = browser.find_element(By.XPATH,
                                                     '/html/body/div[1]/div[2]/div[2]/div[1]/div/div/div[2]/div[3]/div[2]/div[1]/div/div[2]/div[2]/p[1]').text
            except:
                seal_contours = None
            try:
                door_filling = browser.find_element_by_xpath(
                    '/html/body/div[1]/div[2]/div[2]/div[1]/div/div/div[2]/div[3]/div[2]/div[1]/div/div[2]/div[3]/p[2]').text
            except:
                door_filling = None
            try:
                external_panel = browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div/div/div[2]/div[3]/div[2]/div[2]/div[2]/div[2]/p[2]').text.strip()
            except:
                external_panel = None
            try:
                external_panel_1 = browser.find_element(By.XPATH,
                                                        '/html/body/div[1]/div[2]/div[2]/div[1]/div/div/div[2]/div[3]/div[2]/div[2]/div[2]/div[2]/p').text.strip()
            except:
                external_panel_1 = None
            img_external_panel = browser.find_element(By.XPATH,
                                                      '/html/body/div[1]/div[2]/div[2]/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/div/div[1]/a').get_attribute(
                'href')
            thermal_break = ['Да' if 'терморазрыв' in name else 'Нет']
            magnetic_seal = None
            mirror = None
            glazed_window = None
            size = None

            for item_name in browser.find_elements(By.CLASS_NAME, 'product-views__item-inner'):
                internal_panel = item_name.find_element_by_tag_name('img').get_attribute('title')
                img_internal_panel = item_name.find_element_by_tag_name('img').get_attribute('src')
                price = item_name.find_element_by_tag_name('input').get_attribute('value')

                with open('intecron_2.csv', 'a', encoding='UTF-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(
                            (
                                name,
                                price,
                                image,
                                desc,
                                'да',
                                'Intecron',
                                img_external_panel,
                                [external_panel or external_panel_1],
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
    get_page_data('index_2.html')


if __name__ == '__main__':
    main()