# import pandas
import time

import requests
# import csv
from bs4 import BeautifulSoup
from fake_useragent import UserAgent  # pip install fake-useragent
import json
import re
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


def pagination(model, url):
    for page in range(1, 3):
        page_url = f'{url}/?sort=position&direction=asc&page={page}'


# save the page
def get_page(url):
    req = requests.get(url, headers=header)
    src = req.text

    with open('index.html', 'w') as file:
        index = file.write(src)
    return index


# read index.html
def get_data(html):

    
    with open(html) as f:
        src = f.read()
        soup = BeautifulSoup(src, 'lxml')

        menu = soup.select('div.secondary:nth-child(1) > ul:nth-child(1) > li:nth-child(2) > div:nth-child(2) > ul:nth-child(1) > li > a')
        for link in menu:
            url = domain + link.get('href')
            # soup = make_request(url, header)
            browser.get(url)
            time.sleep(5)
            
            links = browser.find_element(By.XPATH, '/html/body/section[5]/div/div/div/div[2]/div[2]')
            print(links)
            # index = soup.find('div', attrs=re.compile('interchange'))
            # for link in index:
            #     link.has_attr('data-interchange')
            #     print(link)
            # 


            # for link in browser.find_elements(By.XPATH, '/html/body/section[5]/div/div/div/div[2]/div[2]/ul/li/a'):
            #     page_links.append(link)
            #
            # links = [link.click() for link in page_links]
            # links = [link.text for link in soup.select('.pagination > li > a')]

            # soup = make_request(url, header)
            # pagination = soup.select('.pagination > li > a')
            # for link in pagination:
            #     link.click()
            # print(pagination)
            # pages = '/katalog/kupit/?arrFilter_pf%5BDOOR_MODEL_APPLY%5D=20256&set_filter=Y&PAGEN_1=2'



        # item_data = []
        # specifications = []
        # for link in soup.find_all('div', class_='card'):
        #     name = link.find('h2', attrs={'itemprop': 'name'}).text
        #     item_urls = domain + link.find('h2', attrs={'itemprop': 'name'}).find('a').get('href')
        #     price = link.find('span', class_='price').text
        #     image = domain + link.find('div', class_='card-image').find('img').get('src')
        #
        #     # get data from item page
        #     req_item_urls = requests.get(item_urls, headers=headers)
        #     items_src = req_item_urls.text
        #     soup = BeautifulSoup(items_src, 'lxml')
        #     short_desc = soup.find('section', id='model-design').find_next('h2').text
        #     img_desc = [domain + img.get('src') for img in soup.find_all('img', attrs={'itemprop': 'contentUrl'})]
        #     long_dec = [desc.text.strip() for desc in soup.find_all('div', attrs={'itemprop': 'description'})]
        #     specification_url = domain + soup.find('a', class_='read-more').get('href')
        #     item_data.append(
        #             {
        #                 'Наименование': name,
        #                 'Панель внешняя': short_desc,
        #                 'Картинка панель внешняя': image,
        #                 'Картинка панель внутренняя': img_desc,
        #                 'Описание товара': long_dec,
        #                 'Цена товара': price,
        #                 'Изображение товара': image,
        #                 'Галерея': img_desc,
        #             }
        #         )
        #     get_json(item_data)
        #
        #     # get specification from specification page
        #     req_specification = requests.get(specification_url, headers=headers)
        #     specification_src = req_specification.text
        #     soup = BeautifulSoup(specification_src, 'lxml')
        #
        #     for row in soup.find('table').find('tbody').find_all('tr'):
        #         col = row.find_all('td')
        #         if len(col) != 1:
        #             title = col[0].text
        #             description = col[1].text.strip().replace('\t', '')
        #
        #             specifications.append(
        #                 {
        #                     title: description
        #                 }
        #             )
        #     get_json(specifications)


def main():
    # get_page(site)
    get_data('index.html')


if __name__ == '__main__':
    main()