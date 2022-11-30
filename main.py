import pandas as pd
import time
import csv
import os
import sys

# Selenium Web Scraping
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

import chromedriver_binary

# SQL Database
import psycopg2
from sqlalchemy import create_engine 

load_dotenv()

def pages(driver):
    load_more = driver.find_elements(By.XPATH, "//div[@x-show='showLoadMore']")[0].text
    print("Loading all items...")
    while load_more == "Load more":
        element = driver.find_elements(By.XPATH, "//div[@class='card-root h-full w-full']/a")[-1]
        driver.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(2)
        driver.find_elements(By.XPATH, "//div[@x-show='showLoadMore']")[0].click()
        time.sleep(3)
        element = driver.find_elements(By.XPATH, "//div[@class='card-root h-full w-full']/a")[-1]
        driver.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(2)
        load_more = driver.find_elements(By.XPATH, "//div[@x-show='showLoadMore']")[0].text

        
def item_scrapper(driver, data):
    time.sleep(1)
    # Store all the links
    item_links = []
    items_elems = driver.find_elements(By.XPATH, "//div[@class='card-root h-full w-full']/a")
    for i in range(0, len(items_elems)):
        item_links.append(items_elems[i].get_attribute('href'))
        
    for i in tqdm(range(0, len(item_links))):
        link_url = item_links[i]
        driver.get(link_url)
        time.sleep(2)
        #WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='mb-8']")))
        category_text = driver.find_elements(By.XPATH, "//div[@class='col-span-5']/div[@class='body-2  !font-semibold']")[0].text
        title_text = driver.find_elements(By.XPATH, "//div[@class='col-span-5']/div[@class='mb-8']/h1")[0].text
        organiser_text = driver.find_elements(By.XPATH, "//div[@class='col-span-5']/div[@class='mb-8']/div[@class='body-2 rte']")[1].text
        date_text = driver.find_elements(By.XPATH, "//div[@class='col-span-5']/div[@class='flex justify-start body-2 mb-8']")[0].text
        address_text = driver.find_elements(By.XPATH, "//div[@class='col-span-5']/div[@class='flex justify-start body-2 mb-8']")[2].text
        link_text = driver.current_url
        
        day_text = ''
        time_text = ''
        
        data.append({'category': category_text,
                    'title': title_text,
                    'link': link_text,
                    'organiser': organiser_text,
                    'date': date_text,
                    'day': day_text,
                    'time': time_text,
                    'address': address_text})
    return data
        
def check_update(df, new_titles, con):
    query = f"""SELECT * FROM data"""
    old_title = list(pd.read_sql(query, con).loc[:,"title"])
    print("Number of old titles: {}".format(len(old_title)))
    for title in list(df["title"]):
        if title not in old_title:
            new_titles.append(title)
    print("Number of new new titles: {}".format(len(new_titles)))
    return new_titles
    
def send_telegram_message(msg, CHAT_ID, API_KEY):
    # start telegram bot
    bot = telegram.Bot(token=API_KEY)
    bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)
    
if __name__ == "__main__":
    
    url = "https://www.esplanade.com/whats-on?performanceNature=Free+Programme"
    API_KEY = os.getenv("API_KEY")
    CHAT_ID = os.getenv("CHAT_ID")
    #DATABASE_URL = os.getenv("DATABASE_URL")
    DATABASE_URL = "postgresql://postgres:ZCrpT0IDtZUsSHrejZk3@containers-us-west-19.railway.app:6464/railway"

    # #set up database
    # if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    #    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    

    engine = create_engine(DATABASE_URL, echo = False)
    con = psycopg2.connect(DATABASE_URL)
    cur = con.cursor()

    # setting up options
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.binary_location = os.getenv("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("disable-dev-shm-usage")
    #driver = webdriver.Chrome("chromedriver.exe", chrome_options=chrome_options)
    #driver = webdriver.Chrome(service=Service(os.getenv("CHROMEDRIVER_PATH")), options=chrome_options)
    driver =  webdriver.Chrome(options=chrome_options)

    driver.get(url)
    WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='card-root h-full w-full']")))
    
    current_site = driver.current_url
    
    #Load more
    print("Getting total pages...")
    pages(driver)
    time.sleep(2)
    
    #Start scraping
    print("Starting to scrape..")
    data = []
    
    data = item_scrapper(driver, data)
    
    print("Scraping complete!")
    df = pd.DataFrame(data)
    
    # Check for new titles
    print("Checking for new titles...")
    new_titles = []
    update = check_update(df, new_titles, con)
    
    # print("Sending telegram notification...")
    # if len(update) != 0:
        
    #     # Get those new titles information
    #     df_update = df[df["title"].isin(update)]
    #     # Get only MUSIC category
    #     df_update = df_update[df_update["category"] == "Music"]
    #     print("Number of new music titles: {}".format(len(df_update)))
    #     # for k in range(len(df_update)):
    #     #     code_html='*{}*'.format(df_update["title"].iloc[k])  
    #     #     msg = code_html + "\n\n *Category:* " + str((df_update["category"].iloc[k])) + "\n *Title:* " + str((df_update["title"].iloc[k])) + "\n *Organiser:* " + str((df_update["organiser"].iloc[k])) + "\n *Date:* " + str((df_update["date"].iloc[k])) + "\n *Address:* " + str((df_update["address"].iloc[k])) + "\n *Link:* " + str((df_update["link"].iloc[k]))
    #     #     time.sleep(2)
    #     #     send_telegram_message(msg, CHAT_ID, API_KEY)

            
    #     # Save to csv
    #     print("Saving database...")
    #     df_update.to_sql('data', con=engine, if_exists="append", index=False)
        
    # else:
    #     msg = "No new updates"
    #     print(msg)
 
    
    
    
    

