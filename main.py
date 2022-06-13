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
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
from tqdm import tqdm
import telegram

import time
import csv
import os
import sys

load_dotenv()

def pages(driver):
    pages_text = driver.find_element(By.XPATH, "//div[@class='paging-container']").text
    if (pages_text.split("\n")[-2].isnumeric()):
        total_pages = pages_text.split("\n")[-2]
    else:
        total_pages = pages_text.split("\n")[-1]
    return total_pages
        
def item_scrapper(driver, data):
    items_elems = driver.find_elements(By.CLASS_NAME, "overlay")
    for i in tqdm(range(0, len(items_elems))):
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
        
def check_update(df, new_titles):
    old_title = list(pd.read_csv("output.csv").loc[:,"title"])
    for title in list(df["title"]):
        if title not in old_title:
            new_titles.append(title)
    return new_titles
    
def send_telegram_message(msg, CHAT_ID, API_KEY):
    # start telegram bot
    bot = telegram.Bot(token=API_KEY)
    bot.send_message(chat_id=CHAT_ID, text=msg)
    
if __name__ == "__main__":
    
    url = "https://www.esplanade.com/whats-on/category"
    API_KEY = os.getenv("API_KEY")
    CHAT_ID = os.getenv("CHAT_ID")
    
    # setting up options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.getenv("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("disable-dev-shm-usage")
    #driver = webdriver.Chrome("chromedriver.exe", chrome_options=chrome_options)
    driver = webdriver.Chrome(service=Service(os.getenv("CHROMEDRIVER_PATH")), options=chrome_options)
    driver.get(url)
    
    # Free events category
    driver.find_element(By.LINK_TEXT, 'Free').click()
    time.sleep(2)
    
    current_site = driver.current_url
    
    # Get total number of pages
    print("Getting total pages...")
    total_pages = pages(driver)
    
    # Start scraping
    print("Starting to scrape..")
    data = []
    for j in range(0, int(total_pages)):
        print("============")
        print("Pages: {}/{}".format(j+1, total_pages))
        print("============")
        page_navigate = "&page={}".format(j)
        url = current_site + page_navigate
        driver.get(url)
        time.sleep(2)
    
        data = item_scrapper(driver, data)
    
    print("Scraping complete!")
    df = pd.DataFrame(data)
    
    # Check for new titles
    print("Checking for new titles...")
    new_titles = []
    update = check_update(df, new_titles)
    
    print("Sending telegram notification...")
    if len(update) != 0:
        code_html='*NEW FREE PERFORMANCES IN ESPLANADE*'  
        df_update = df[df["title"].isin(update)]
        for k in range(len(df_update)):
            msg = code_html + "\n\n Category: " + str((df_update["category"].iloc[k])) + "\n Title: " + str((df_update["title"].iloc[k])) + "\n Organiser: " + str((df_update["organiser"].iloc[k])) + "\n Date: " + str((df_update["date"].iloc[k])) + "\n Day: " + str((df_update["day"].iloc[k])) +  "\n Time: " + str((df_update["time"].iloc[k])) + "\n Address: " + str((df_update["address"].iloc[k])) + "\n Link: " + str((df_update["link"].iloc[k]))
            send_telegram_message(msg, CHAT_ID, API_KEY, parse_mode= 'Markdown')
        
    # Save to csv
    df.to_csv("output.csv")
    
    
    

