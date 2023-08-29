
from bs4 import BeautifulSoup
import requests
import time

# Find newly published jesey listings

def VFSScraper():
    try:
        URL = "https://www.vintagefootballshirts.com/new-products/"
        result = requests.get(URL)

        # Scrape all listings on "New products" page
        soup = BeautifulSoup(result.content, 'html.parser')
        jerseysListVFS = soup.find('div', id="content").find_all("div", class_="col4")

        for jersey in jerseysListVFS:
            link = jersey.find('a')['href']
            price = jersey.find('span').text
            print(link)
            print(price)
        
    # Error
    except Exception as e:
        print(e)

def VFAScraper():
    try:
        # baseURL not included in href, so concatenate it manually
        baseURL='https://www.vintagefootballarea.com'
        URL = "https://www.vintagefootballarea.com/collections/tous-les-maillots"
        result = requests.get(URL)

        # Scrape all listings on "Our collection" page
        soup = BeautifulSoup(result.content, 'html.parser')
        jerseysListVFA = soup.find('div', class_='collection-listing cf').find_all('div', class_='innerer')

        for jersey in jerseysListVFA:
            name = jersey.find('div', class_='title').text
            link = baseURL + jersey.find('a', class_='product-link')['href']
            price = jersey.find('span', class_='price').find('span', class_='theme-money').text        
        
    # Error
    except Exception as e:
        print(e)


VFSScraper()