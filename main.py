import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait as wait

import time
import csv
import os
import sys

def pages(driver):
    pages_text = driver.find_element(By.XPATH, "//div[@class='paging-container']").text
    if (pages_text.split("\n")[-2].isnumeric()):
        total_pages = pages_text.split("\n")[-2]
    else:
        total_pages = pages_text.split("\n")[-1]
    return total_pages
        
def item_scrapper(driver, data):
    items_elems = driver.find_elements(By.CLASS_NAME, "overlay")
    for i in range(0, len(items_elems)):
        items_elems[i].click()
        
        WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='event-header']")))
        category_elem = driver.find_element(By.XPATH, "//div[@class='event-header']").text
        category_text = category_elem.split("\n")[1]

        title_text = driver.find_element(By.TAG_NAME, "h1").text

        organiser_text = driver.find_element(By.CLASS_NAME, "event-organizer").text

        date_elem = driver.find_element(By.XPATH, "//div[@class='event-date-partial']/div[@itemprop='startDate']").text
        date_text = date_elem.split("\n")[0]
        
        try:
            day_text = date_elem.split("\n")[1]
        except:
            print("No Day")
            day_text = None
            
        time_text = driver.find_element(By.XPATH, "//div[@class='event-date-partial']/div[@itemprop='doorTime']").text
        address_text = driver.find_element(By.CLASS_NAME, "address").text
        link_text = driver.current_url
        
        data.append({'category': category_text,
                    'title': title_text,
                    'link': link_text,
                    'organiser': organiser_text,
                    'date': date_text,
                    'day': day_text,
                    'time': time_text,
                    'address': address_text})
        
        driver.back()
    return data
        
if __name__ == "__main__":
    
    url = "https://www.esplanade.com/whats-on/category"

    # setting up options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome("chromedriver.exe", options=chrome_options)
    driver.get(url)
    
    # Free events category
    driver.find_element(By.LINK_TEXT, 'Free').click()
    time.sleep(2)
    
    current_site = driver.current_url
    
    # Get total number of pages
    total_pages = pages(driver)

    # Start scraping
    data = []
    for j in range(0, int(total_pages)):
        page_navigate = "&page={}".format(j)
        url = current_site + page_navigate
        driver.get(url)
        time.sleep(2)
    
        data = item_scrapper(driver, data)
    
    df = pd.DataFrame(data)
    
    # Save to csv
    df.to_csv("output.csv")
    

    
    

