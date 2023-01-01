import telegram
import os 
from dotenv import load_dotenv

# Custom Message
load_dotenv()

API_KEY = os.getenv("API_KEY")
CHAT_ID = os.getenv("CHAT_ID")
    
def send_telegram_message(msg, CHAT_ID, API_KEY):
    # start telegram bot
    bot = telegram.Bot(token=API_KEY)
    bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)
    
if __name__ == "__main__":
    msg = "Apologies for the spam. Database has been updated."
    send_telegram_message(msg, CHAT_ID, API_KEY)