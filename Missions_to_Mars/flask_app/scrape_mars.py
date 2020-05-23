# Dependencies and Setup
from bs4 import BeautifulSoup
from splinter import Browser


# Initialize browser
def init_browser(): 
    #Replace the path with your actual path to the chromedriver
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
    # Create global dictionary that can be imported into Mongo
    mars_info = {}

    try: 
        # Initialize browser 
        browser = init_browser()
        #browser.is_element_present_by_css("div.content_title", wait_time=1)

        #################################################
        # Nasa Mars News
        #################################################
        # Visit Nasa news url
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        # HTML Object
        html = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')

        # Retrieve latest News Title and Paragraph Text
        news_title = soup.find('div', class_='list_text')
        news_p = soup.find('div', class_='article_teaser_body').text
        news_title_txt = news_title.find("a").text

        # Dictionary entry from MARS NEWS
        mars_info['news_title'] = news_title_txt
        mars_info['news_paragraph'] = news_p


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

        # Scrape the latest Mars weather tweet from the page
        latest_mars_weather = weather_soup.find('div', class_ = "css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")
        
        # Save the latest Mars weather tweet
        mars_weather = latest_mars_weather.find("span").text

        mars_info['mars_weather'] = mars_weather


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

        # Return mars_data dictionary 
        return mars_info

    finally:
        browser.quit()
    