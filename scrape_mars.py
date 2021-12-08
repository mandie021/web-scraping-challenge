from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import ssl
import requests


# setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

def scrape():
    # browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser3 = Browser('chrome', **executable_path, headless=False)
    mars_url = 'https://marshemispheres.com/'
    browser3.visit(mars_url)
    html = browser3.html
    soup = bs(html, "html.parser")

    hemisphere_image_urls = {}
    hemisphere_image_urls['title'] = []
    hemisphere_image_urls['img_url'] = []
    for item in product_search:
        img_search=soup.find('img', class_='thumb')
        hemisphere_image_urls['img_url'].append('https://marshemispheres/' + img_search['src'])
        title_search=soup.find('h3').text
        hemisphere_image_urls['title'].append(title_search)
        print(hemisphere_image_urls)


    
    # Quit the browser
    browser.quit()

    return hemisphere_image_urls