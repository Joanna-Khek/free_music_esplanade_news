import os
from dotenv import load_dotenv
import requests

load_dotenv()

TELEGRAM_API_KEY = os.getenv("API_KEY")
TELEGRAM_GROUP_ID = "band-news-esplanade"

def send_msg_on_telegram(message):
    telegram_api_url = f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage?chat_id=@{TELEGRAM_GROUP_ID}&text={message}"
    tel_resp = requests.get(telegram_api_url)
    
    if tel_resp.status_code == 200:
        print("INFO: Notification has been sent on Telegram")
    else:
        print("ERROR: Could not send Message")
        
send_msg_on_telegram("TEST")