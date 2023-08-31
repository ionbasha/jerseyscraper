
from bs4 import BeautifulSoup
import requests
import os
from pymongo import MongoClient

#new_listings = 0
connection_string = 'mongodb://localhost:27017/'
client = MongoClient(connection_string)
db = client.jerseyscraper_db
collection = db.jersey_info

# Find newly published jesey listings

def VFSScraper():
    try:
        # Since the VFS website may add many jerseys to the site at a time,
        # search first AND second page for any new additions
        for i in range(1,3):
            URL = "https://www.vintagefootballshirts.com/new-products/?page="+str(i)
            result = requests.get(URL)

            # Scrape all listings on "New products" page
            soup = BeautifulSoup(result.content, 'html.parser')
            jerseysListVFS = soup.find('div', id="content").find_all("div", class_="col4")

            # Collect name, price and link
            for jersey in jerseysListVFS:
                name = jersey.find('img')['alt']
                link = jersey.find('a')['href']
                price = jersey.find('span').text

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

        # Collect name, price and link
        for jersey in jerseysListVFA:
            name = jersey.find('div', class_='title').text
            link = baseURL + jersey.find('a', class_='product-link')['href']
            price = jersey.find('span', class_='price').find('span', class_='theme-money').text        

    except Exception as e:
        print(e)

# Send desktop notification when finished
def send_notification(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))

# Run scrapers and send desktop notification with updates
""" if __name__ == "__main__":
    VFAScraper()
    VFSScraper()
    ttl = "jerseyscraper finished"
    msg = f"{new_listings} new listings scraped"   
    send_notification(ttl, msg)
 """