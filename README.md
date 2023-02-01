# Free Music @ Esplanade News
[![Esplanade News Scrapper](https://github.com/Joanna-Khek/free_music_esplanade_news/actions/workflows/action.yml/badge.svg)](https://github.com/Joanna-Khek/free_music_esplanade_news/actions/workflows/action.yml)

![free mUSIC](https://user-images.githubusercontent.com/53141849/173496469-5b5c920e-5ce0-4e1f-b38e-edcfa2b1f25f.png)

## Inspiration
My partner and I are both musicians and we love attending music performances together. The Esplanade Singapore frequently organises free music performances and we thought it will be great if we can get notifications of any new upcoming performances as soon as possible since some performances require registration and tickets might be snapped up fast!

## Project Description
### 1. Web Scraping
- I built a web scraping script that scrapes all "free" performances at the esplanade and saved it in a database. The script is written in Python and uses Selenium.

![new_esplanade](https://user-images.githubusercontent.com/53141849/178405333-513130db-6c8c-459d-9004-58380c9e7583.png)

### 2. Telegram Bot

- I built a telegram bot that takes in the newly scraped data and compares with the past data stored in the database. The bot will return only those newly added performances under the "MUSIC" category.
![screenshot](https://user-images.githubusercontent.com/53141849/173495469-371306a9-5e49-4e02-bd89-0b483b2b404c.png)

### 3. Deployment
- I scheduled a cron job using github actions to run the script every hour.

- Feel free to join the group! https://t.me/+F9x8L7z_Msw3MDQ1

