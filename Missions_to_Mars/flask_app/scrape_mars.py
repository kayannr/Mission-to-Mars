# Dependencies and Setup
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests


# Initialize browser
def init_browser(): 
    #Replace the path with your actual path to the chromedriver
    # Set executable path & assign Chrome Browser
    # executable_path = {'executable_path': './chromedriver.exe'}
    # browser = Browser('chrome', **executable_path, headless=False)
    import os
    if os.name=="nt":
        executable_path = {'executable_path': './chromedriver.exe'}
    else:
        executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

#################################################
# Function Returns All NASA Scraped Data
#################################################
def scrape():
    # Create global dictionary that can be imported into MongoDB
    mars_info = {}
    try: 
        # Initialize browser using function above 
        browser = init_browser()

        #################################################
        # Nasa Mars News
        #################################################
        #browser.is_element_present_by_css("div.content_title", wait_time=1)
        # Visit Nasa news url
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        # HTML Object
        html_news = browser.html

        # Parse HTML with Beautiful Soup
        news_soup = BeautifulSoup(html_news, 'html.parser')

        # Retrieve latest News Title and Paragraph Text
        news_title = news_soup.find('div', class_='list_text')
        news_p = news_soup.find('div', class_='article_teaser_body')
        news_paragraph=news_p.text
        news_title_txt = news_title.find("a").text

        # Dictionary entry from MARS NEWS
        mars_info['news_title'] = news_title_txt
        mars_info['news_paragraph'] = news_paragraph


        #################################################
        # Mars Featured Image
        #################################################
        # Visit Mars Space Images URL
        featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(featured_image_url)

        # HTML Object 
        html_image = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html_image, 'html.parser')

        # Retrieve the image url for the current Featured Mars Image from style tag 
        featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
        
        # Main Url 
        main_url = 'https://www.jpl.nasa.gov'

        # Concatenate main url with scraped route
        featured_image_url = main_url + featured_image_url

        mars_info['featured_image_url'] = featured_image_url


        #################################################
        # Mars Weather
        #################################################
        # Visit Mars Weather Twitter through splinter module
        weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_url)

        # HTML Object 
        html_weather = browser.html

        # Parse HTML with Beautiful Soup
        weather_soup = BeautifulSoup(html_weather, 'html.parser')

        weather_tweets = weather_soup.find_all('span')
        # Print weather_tweets

        # Retrieve all elements that contain tweet text in the specified range
        # Look for entries that display weather related words to exclude non weather related tweets 
        for tweet in weather_tweets: 
            mars_weather_tweet = tweet.text
            if 'InSight sol' and 'pressure' in mars_weather_tweet:
                # print(f"{mars_weather_tweet}")
                print(mars_weather_tweet)
                break
            else: 
                pass
        # Save to dictionary
        mars_info['weather_mars']  = str(mars_weather_tweet)
        
        #################################################
        # Mars Facts
        #################################################
        # Visit the Mars Facts Site Using Pandas to Read
        mars_df = pd.read_html("https://space-facts.com/mars/")[0]

        # Assign the columns amd set index
        mars_df.columns=["Description", "Value"]
        mars_df.set_index("Description", inplace=True)
        
        # Save html code to folder Assets
        mars_data = mars_df.to_html()

        mars_info['mars_facts'] = mars_data


        #################################################
        # Mars Hemispheres
        #################################################
        # Visit USGS Astrogeology Science Center Website
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)

        # HTML Object
        html_hemispheres = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html_hemispheres, 'html.parser')

        # Retreive all items that contain mars hemispheres information
        items = soup.find_all('div', class_='item')

        # Create empty list for hemisphere urls 
        hemisphere_image_urls = []

        # main_url 
        hemispheres_main_url = 'https://astrogeology.usgs.gov'

        # Loop through the items 
        for i in items: 
            title = i.find('h3').text
            
            # Store link to full image website
            img_url = i.find('a', class_='itemLink product-item')['href']
            
            # Visit the link that contains the full image website 
            browser.visit(hemispheres_main_url + img_url)
            
            # HTML Object of individual hemisphere info website 
            img_html = browser.html
            
            # Parse HTML with Beautiful Soup for every individual hemisphere information website 
            soup = BeautifulSoup( img_html, 'html.parser')
            
            # Retrieve full image source 
            img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            
            # Append the retreived information into a list of dictionaries 
            hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

        mars_info['hemisphere_image_urls']=hemisphere_image_urls

        browser.quit()
        # Return mars_data dictionary 
        return mars_info

    finally:
        browser.quit()

print(scrape())