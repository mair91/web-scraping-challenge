import pandas as pd
from splinter import Browser
import requests
from bs4 import BeautifulSoup

def init_browser(): 
    executable_path = {'executable_path': 'chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

marsInfo ={}

def scrape_news():
    browser = init_browser()
    newsURL = 'https://mars.nasa.gov/news/'
    browser.visit(newsURL)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_titles = soup.find_all('div', class_='content_title')
    news_title = news_titles[1].text
    news_p = soup.find_all('div', class_='article_teaser_body')
    news_p = news_p[0].text
    print(news_title + news_p)
    #marsInfo['news_title'] = news_title
    #marsInfo['news_paragraph'] = news_p
    marsInfo = {
        "news_title": news_title,
        "news_paragraph": news_p
    }

    browser.quit()
    
    return marsInfo

def scrape_image():
    browser = init_browser()
    imageURL = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(imageURL)
    main = 'https://www.jpl.nasa.gov'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    featured_image_url = main + featured_image_url
    featured_image_url
    marsInfo = {
        "featured_image_url": featured_image_url
    }
    
    browser.quit()

    return marsInfo

def scrape_weather():
    browser = init_browser()
    weatherURL = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weatherURL)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    LT = soup.find_all('div', class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0')
    last_tweet = LT[0].text
    marsInfo = {
        "weatherTweet": last_tweet
    }
    
    browser.quit()
    
    return marsInfo

def scrape_facts():
    browser = init_browser()
    marsFacts = 'https://space-facts.com/mars/'
    marsFactsTable = pd.read_html(marsFacts)
    marsFactsDF = marsFactsTable[0]
    marsFactsDF.columns = ['Facts', 'Value']
    marsFactsDF.set_index('Facts', inplace=True)
    HTMLtable = marsFactsDF.to_html()
    marsInfo = {
        "marsFacts": HTMLtable
    }
    
    browser.quit()

    return marsInfo

def scrape_hemi():
    browser = init_browser()
    USGSurl="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    USGSMainURL="https://astrogeology.usgs.gov"
    browser.visit(USGSurl)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    marsImages = soup.find_all('div', class_='item')
    hemisphereURL = []

    for i in marsImages: 
        title = i.find('h3').text
        shortURL = i.find('a', class_='itemLink product-item')['href']
        browser.visit(USGSMainURL + shortURL)
        shortURL = browser.html
        soup = BeautifulSoup(shortURL, 'html.parser')
        imguRL = USGSMainURL + soup.find('img', class_='wide-image')['src']
        hemisphereURL.append({"Title" : title, "URL" : imguRL})

    marsInfo['hemisphereURL'] = hemisphereURL

    browser.quit()

    return marsInfo 