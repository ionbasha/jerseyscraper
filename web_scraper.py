
from bs4 import BeautifulSoup
import requests
import os
from pymongo import MongoClient

# Gather total number of new items added to database
total_listings_added = 0

connection_string = 'mongodb://localhost:27017/'
client = MongoClient(connection_string)
db = client.jerseyscraper_db
collection = db.jersey_info


# Find newly published jesey listings

def VFSScraper():
    new_listings = 0  
    try:
        # Since the VFS website may add many jerseys to the site at a time,
        # search first three pages for any new additions
        for i in range(1,4):
            URL = SOME_URL
            result = requests.get(URL)

            # Scrape all listings on "New products" page
            soup = BeautifulSoup(result.content, 'html.parser')
            jerseysListVFS = soup.find('div', id="content").find_all("div", class_="col4")

            # Collect name, price and link
            for jersey in jerseysListVFS:
                name = jersey.find('img')['alt']
                link = jersey.find('a')['href']
                price = jersey.find('span').text
                new_listings += db_add(name, link, price)

    except Exception as e:
        print(e)

    return new_listings

def VFAScraper():
    new_listings = 0  
    try:
        baseURL= SOME_baseURL
        # baseURL not included in href, so concatenate it manually
        # Search first three pages for new items
        for i in range(1,4):
            URL = SOME_URL2
            result = requests.get(URL)

            # Scrape all listings on "Our collection" page
            soup = BeautifulSoup(result.content, 'html.parser')
            jerseysListVFA = soup.find('div', class_='collection-listing cf').find_all('div', class_='innerer')

            # Collect name, price and link
            for jersey in jerseysListVFA:
                name = jersey.find('div', class_='title').text
                link = baseURL + jersey.find('a', class_='product-link')['href']
                price = jersey.find('span', class_='price').find('span', class_='theme-money').text        
                new_listings += db_add(name, link, price)

    except Exception as e:
        print(e)

    return new_listings    

# Send desktop notification when finished
def send_notification(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))

# Returns 1 if no duplicate item found and adds new item to database
# Returns 0 if duplicate item found, nothing new added to database
def db_add(name, URL, cost):
    # Create new document only if no duplicates found
    if collection.find_one({'URL': URL}) == None:
        new_doc = {
            'name': name,
            'URL': URL,
            'price': cost
        }
        collection.insert_one(new_doc)
        return 1
    else:
        return 0

# Run scrapers and send desktop notification with updates
if __name__ == "__main__":
    total_listings_added += VFAScraper() # VFA new listings added to total
    total_listings_added += VFSScraper() # VFS new listings added to total
    ttl = "jerseyscraper finished"
    msg = f"{total_listings_added} new listings found"   
    send_notification(ttl, msg) # Print finished message including the number of new listings added
