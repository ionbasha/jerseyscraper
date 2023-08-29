
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
            print(link)
        
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
        jerseysListVFA = soup.find('div', class_='collection-listing cf').find_all('div', class_='product-block detail-mode-permanent')

        for jersey in jerseysListVFA:
            link = baseURL + jersey.find('a', class_='product-link')['href']
            print(link)
        
    # Error
    except Exception as e:
        print(e)

while(True):
    VFAScraper()
    time.sleep(20)
