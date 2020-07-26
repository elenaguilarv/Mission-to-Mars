# Import Splinter and BeautifulSoup dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    
    news_title, news_paragraph = mars_news(browser)
    
    # Create data dictionary: run all scraping functions and store results
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemisphere(browser)
    }
    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser): # call browser variable to automate function

    # Visit and scrape mars nasa news site - assign the url and instruct browser to visit
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    # Searching for specific elements of tag combination - <ul class=”item_list”> in HTML
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    # Set variable for parent element which will hold all other variables within it
    # will be references when filtering results further
    slide_elem = news_soup.select_one('ul.item_list li.slide')

    # Add try/except for AttributeError handling - if found and starting over it will ignore
    try:
    # Scraping for Title of recent article
        slide_elem.find("div", class_='content_title')
    # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
    # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None

    return news_title, news_p

def featured_image(browser):

    ### Featured Images
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that - find element using text
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except block for AttributeError handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    # Find the relative image url using <figure/> & (class=lede),<a/> (nested), and <img/>(nested) - because image is updated frequently
    # This is where the image we want lives-use the link that's inside these tags"

    except AttributeError:
        return None    

    # Use the base URL to create an absolute URL using a new variable to hold our f-string of our other image variable
    # f strings useful for scraping bc they are evaluated at run-time
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    
    return img_url

# Add try/except block for AtrributeError handling
def mars_facts():

# Import pandas to scrape the entire table of Mars facts 
# By creating a new data frame [0] index to pull only the first table it encounters
    try:
        # Use read_html to scrape the facts table into df
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
         return None

    # Assign new columns to the df and turning description column into the index with inplace=True
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Converting df back to HTML code so changes on tables are updated when code is run (add bootstrap)
    return df.to_html(classes="table table-striped")

def hemisphere(browser):
# Scrape 4 high resolution images of Mars
# URL

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)      
    
    hemis_images = []

    for i in range(4,8):

        # Find and click the image
        thumb_image = browser.find_by_tag('img')
        thumb_image[i].click()

        # Parse the resulting html with soup
        html = browser.html
        img_soup = soup(html, 'html.parser')
        
        # Store image URLs and titles in a list
        img_url = img_soup.find('a', text='Sample').get("href") # get pulls the link to the image
        img_title = img_soup.find('h2','title').text
        
        hemis_images.append({"title": img_title, "url": img_url})
        
        browser.back()
        
    return hemis_images

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())   

# End the automated browsing session
# To fully automate the code created above it must be converted into a .py file
    browser.quit()

