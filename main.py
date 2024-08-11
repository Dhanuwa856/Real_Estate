# ---> Requirements:
# Language: Python
# Libraries: BeautifulSoup, Requests, Pandas, SQLite (for database storage)
# Website: Choose a real estate site like Zillow (ensure it’s allowed by the site's robots.txt).
# Data to Collect:
# Property Title
# Price
# Location (Address, City, State)
# Number of Bedrooms and Bathrooms
# Size (Square Footage)
# Listing URL
# Agent/Agency Name (if available)

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import os

# Set up the Chrome WebDriver
os.environ['PATH'] += r"C:\Python"
driver = webdriver.Chrome()

#  Define the URL
base_url = "https://www.zillow.com/los-angeles-ca/houses/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22west%22%3A-119.257679765625%2C%22east%22%3A-117.565785234375%2C%22south%22%3A33.47067625912617%2C%22north%22%3A34.56791831480504%7D%2C%22usersSearchTerm%22%3A%22Los%20Angeles%2C%20CA%22%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A12447%2C%22regionType%22%3A6%7D%5D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A9%7D"

# Open the url
driver.get(base_url)
# wait for the page to load
time.sleep(3)

# Extract data
land_listing = []
target_listing = 1000

while len(land_listing) < target_listing:
  # Find all the listings on the current page
  land_containers = driver.find_elements(By.CSS_SELECTOR,'ul.List-c11n-8-102-0__sc-1smrmqp-0.StyledSearchListWrapper-srp-8-102-0__sc-1ieen0c-0.kquqgw.gLCZxh.photo-cards.photo-cards_extra-attribution li')
  
  for container in land_containers:
    if len(land_listing) >= target_listing:
      break
    
    # extract price
    try:
      price_text = container.find_element(By.CSS_SELECTOR,'span.PropertyCardWrapper__StyledPriceLine-srp-8-102-0__sc-16e8gqd-1.vjmXt')
      price = price_text.text.strip()
    except:
      pass
      
    # extract address
    try:
      address = container.find_element(By.TAG_NAME,'address').text.strip()
    except:
      pass
    # extract Bedrooms
    try:
      bedrooms = container.find_element(By.CSS_SELECTOR,'ul.StyledPropertyCardHomeDetailsList-c11n-8-102-0__sc-1j0som5-0.exCsDV li:nth-child(1)').text.strip()
    except:
      pass 
      
    # extract Bathrooms
    try:
     Bathrooms = container.find_element(By.CSS_SELECTOR,'ul.StyledPropertyCardHomeDetailsList-c11n-8-102-0__sc-1j0som5-0.exCsDV li:nth-child(2)').text.strip()
    except:
     pass
     
    # extract Square Footage 
    try: 
     size = container.find_element(By.CSS_SELECTOR,'ul.StyledPropertyCardHomeDetailsList-c11n-8-102-0__sc-1j0som5-0.exCsDV li:nth-child(3)').text.strip()
    except:
     pass
     
    # extract url
    try:
      url_element = container.find_element(By.TAG_NAME,'a')
      url = url_element.get_attribute('href')
        
    except:
      pass
      
    # extract Agency Name
    try:
     agency_name = container.find_element(By.CSS_SELECTOR,'div.StyledPropertyCardDataArea-c11n-8-102-0__sc-10i1r6-0.eYtsWk').text.strip()
    except:
      pass
    land_listing.append((price,address,bedrooms,Bathrooms,size,url,agency_name))  
    
#Close the WebDriver
driver.quit() 
    
# Save data to a DataFrame
df = pd.DataFrame(land_listing,columns=['Price','Address','Bedrooms','Bathrooms','Square Footage',"URL","Agency Name"])   
df.to_excel("los_angeles_land_listings_filtered.xlsx",index=False)

print("Data scraping completed and saved to los_angeles_land_listings_filtered.xlsx") 

