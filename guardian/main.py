import time
import itertools
import requests
import csv
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


site = 'https://guardian.ru/katalog/'
domain = 'https://guardian.ru'
header = {
    'User-Agent': ua.random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
}


def make_request(url, header):
    req = requests.get(url, headers=header)
    res = req.text
    soup = BeautifulSoup(res, 'lxml')
    return soup


def get_data():
    with open('guardian.csv', 'w', encoding='UTF-8') as file:
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

    with open('links.txt') as f:
        base_urls = ''.join(f.readlines()).strip().split('\n')
        urls = [i for i in base_urls]

        for url in urls:
            soup = make_request(url, header)
            pages = int(soup.find('ul', class_='pagination').find_all('a')[-2].text)

            for page, link in itertools.product(range(1, 3), urls): # pages + 1
                url = link.replace('%D0%A4%D0%B8%D0%BB%D1%8C%D1%82%D1%80&set_filter=Y', '')
                page_url = f'{url}Y&PAGEN_1={page}'
                soup = make_request(page_url, header) # get page 1 - ....
                for item in soup.find_all('div', class_='card-section'):
                    item_url = domain + item.find('a').get('href')

                    # get items data
                    browser.get(item_url)
                    time.sleep(1)
                    name = browser.find_element(By.XPATH, '//h1[contains(@class, "h2 margin-top-empty")]').text
                    price = browser.find_element(By.XPATH, '//span[contains(@class, "price")]').text
                    image_out = browser.find_element(By.XPATH, '/html/body/section[5]/div/div/div[1]/div/div[1]/div[1]/a').get_attribute('href')
                    image_in = browser.find_element(By.XPATH, '/html/body/section[5]/div/div/div[1]/div/div[1]/div[2]/p[1]/a').get_attribute('href')
                    image = (image_out, image_in)

                    browser.find_element(By.XPATH, '//*[text()="Характеристики"]').click()
                    time.sleep(3)
                    desc = browser.find_element(By.XPATH, '/html/body/section[5]/div/div/div[2]/div[2]/div/section/table').text
                    manufacturer = browser.find_element(By.XPATH, '//*[contains(text(),"Производитель")]//following-sibling::td').text
                    try:
                        external_panel = browser.find_element(By.XPATH, '//*[contains(text(),"Отделка снаружи")]//following-sibling::td').text
                    except:
                        external_panel = None
                    img_external_panel = image_out
                    img_internal_panel = image_in
                    internal_panel = browser.find_element(By.XPATH, '//*[contains(text(),"Отделка изнутри")]//following-sibling::td').text
                    metal_thickness = browser.find_element(By.XPATH, '//*[contains(text(),"Толщина полотна двери")]//following-sibling::td').text
                    seal_contours = browser.find_element(By.XPATH, '//*[contains(text(),"Количество контуров")]//following-sibling::td').text
                    size = browser.find_element(By.XPATH, '//*[contains(text(),"Типовые размеры")]//following-sibling::td').text
                    door_filling = browser.find_element(By.XPATH, '//*[contains(text(),"Наполнитель дверного полотна")]//following-sibling::td').text
                    try:
                        external_panel_ = ['Да' if 'металл' in external_panel else 'Нет']
                    except:
                        external_panel_ = None
                    glazed_window = None
                    mirror = None
                    thermal_break = None
                    magnetic_seal = None
                    gallery = None


                    with open('guardian.csv', 'a', encoding='UTF-8') as file:
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
    get_data()


if __name__ == '__main__':
    main()