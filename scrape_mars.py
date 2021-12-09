from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
#import ssl
#import requests


# setup mongo connection
#conn = "mongodb://localhost:27017"
#client = pymongo.MongoClient(conn)

def main_scrape():
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    news_title, news_p = mars_news(browser)
    feature_img = space_feat(browser)
    mars_web, mars_earth_web = mars_facts()
    hemisphere_image_urls = img_scrape(browser)


    mars_data= {
                "news_title" : news_title, 
                "news_p" : news_p, 
                'feature_img' : feature_img,
                "mars_web" : mars_web,
                "mars_earth_web" : mars_earth_web,
                "hemisphere_img_urls" : hemisphere_image_urls
                }

    # Quit the browser
    browser.quit()

    return mars_data

    

def mars_news(browser):
    ##url 
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    #beautiful soup
    html = browser.html
    soup = bs(html, "html.parser")

    cl_row = soup.select_one('div.row')
    #grab news title
    news_title= cl_row.select_one('div.content_title').text
    #grab news paragrath
    news_p = cl_row.select_one('div.article_teaser_body').text

    return news_title, news_p

def space_feat(browser):
    #url
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    #beautiful soup
    html = browser.html
    soup = bs(html, "html.parser")

    results = soup.find('img', class_="headerimage")
    img_src = results.attrs['src']
    featured_image_url = url+img_src

    return featured_image_url


def mars_facts(): 
    #url
    url = 'https://galaxyfacts-mars.com/'
    mars_tables = pd.read_html(str(url), header=None, index_col=None)
    mars_info = mars_tables[1]
    mars_info.columns = ["Mars Profile", "Measure"]
    mars_web = mars_info.to_html()
    mars_earth_info = mars_tables[0]
    mars_earth_info.columns = ["Mars - Earth Comparison", "Mars", "Earth"]
    mars_earth_web = mars_earth_info.to_html()

    return mars_web, mars_earth_web


def img_scrape(browser):
    # url % beautiful soup 
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")

    hemisphere_image_urls = []

    for item in range(4):
        browser.find_by_css('a.product-item h3')[item].click()
        sample = browser.find_link_by_text('Sample').first
        img_url = sample['href']
        title_search=browser.find_by_css("h2.title").text
        hemisphere_image_urls.append({"title": title_search,'img_url':'https://marshemispheres/' + img_url})
        print(hemisphere_image_urls)
        browser.back()

    return hemisphere_image_urls
    
    

    