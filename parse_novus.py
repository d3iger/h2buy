import requests
from sqlite import sqlight
import config
import requests
from bs4 import BeautifulSoup


url_mn = 'https://novus.zakaz.ua'
url_mn2 = 'https://novus.zakaz.ua/ru/'

db = sqlight(r'./db/parse_novus.db')


HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}





def get_html_for_url(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    res = r.text
    return res

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('a', class_='Pagination__item')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1



def get_url(html, url_mn):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('li', class_='jsx-1852869390')
    url_list = []
    for item in items:
        url2 = item.find('a', class_='jsx-1852869390 CategoriesMenuListItem__link')['href']
        url_list.append(url_mn + url2)
    print(url_list)
    return url_list


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='jsx-33926795 ProductsBox__listItem')

    products = []
    for item in items:
        price = item.find('span', class_='jsx-3642073353 Price__value_caption Price__value_discount')
        price2 = item.find('span', class_='jsx-3642073353 Price__value_caption')
        if price:
            price = price.get_text()
        elif price2:
            price = price2.get_text()
        else:
            price = "0"
        products.append({
            'title': item.find('span', class_='jsx-2958303393 ProductTile__title').get_text(),
            'price': price,
        })
    return products

async def parse():
    id = 0
    db.delete()
    url_lst = get_url(get_html_for_url(url_mn2, params=None), url_mn)
    for url in range(len(url_lst)):
        html = get_html(url_lst[url])
        if html.status_code == 200:
            products = []
            pages_count = get_pages_count(html.text)
            for page in range(1, pages_count + 1):
                print("Parse")
                html = get_html(url_lst[url], params={'page': page})
                products.extend(get_content(html.text))
            print(products)

            for product in products:
                if not db.get_price(product['title']):
                    id += 1
                    db.save_file(product['title'], product['price'], product['title'].lower(), id)


        else:
            print("ERROR")