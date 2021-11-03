# import pandas
import requests
# import csv
from bs4 import BeautifulSoup
import json
# import re


site = 'https://guardian.ru/stalnye_dveri/'
domain = 'https://guardian.ru'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
}


def get_json(lst):
    with open('file.json', 'w') as file:
        # indent - отступы, ensure_ascii - убирает символы и позволяет устранить проблемы с кодировкой
        json.dump(lst, file, indent=4, ensure_ascii=False)
        return json


# save the page
def get_page(url):
    req = requests.get(url, headers=headers)
    src = req.text

    with open('index.html', 'w') as file:
        index = file.write(src)
    return index


# read index.html
def get_data(html):

    with open(html) as f:
        src = f.read()
        soup = BeautifulSoup(src, 'lxml')

        item_data = []
        specifications = []
        for link in soup.find_all('div', class_='card'):
            name = link.find('h2', attrs={'itemprop': 'name'}).text
            item_urls = domain + link.find('h2', attrs={'itemprop': 'name'}).find('a').get('href')
            price = link.find('span', class_='price').text
            image = domain + link.find('div', class_='card-image').find('img').get('src')

            # get data from item page
            req_item_urls = requests.get(item_urls, headers=headers)
            items_src = req_item_urls.text
            soup = BeautifulSoup(items_src, 'lxml')
            short_desc = soup.find('section', id='model-design').find_next('h2').text
            img_desc = [domain + img.get('src') for img in soup.find_all('img', attrs={'itemprop': 'contentUrl'})]
            long_dec = [desc.text.strip() for desc in soup.find_all('div', attrs={'itemprop': 'description'})]
            specification_url = domain + soup.find('a', class_='read-more').get('href')
            item_data.append(
                    {
                        'Наименование': name,
                        'Панель внешняя': short_desc,
                        'Картинка панель внешняя': image,
                        'Картинка панель внутренняя': img_desc,
                        'Описание товара': long_dec,
                        'Цена товара': price,
                        'Изображение товара': image,
                        'Галерея': img_desc,
                    }
                )
            get_json(item_data)

            # get specification from specification page
            req_specification = requests.get(specification_url, headers=headers)
            specification_src = req_specification.text
            soup = BeautifulSoup(specification_src, 'lxml')

            for row in soup.find('table').find('tbody').find_all('tr'):
                col = row.find_all('td')
                if len(col) != 1:
                    title = col[0].text
                    description = col[1].text.strip().replace('\t', '')

                    specifications.append(
                        {
                            title: description
                        }
                    )
            get_json(specifications)


def main():
    get_page(site)
    get_data('index.html')


if __name__ == '__main__':
    main()