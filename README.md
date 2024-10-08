# Betting Events Scraper

## Description
This is a bot that finds surebets from 3 bookmakers (wplay,betplay and codere), orders the info and look for surebets. When any surebet is found, send it throught a telegram bot

![](prematch_bettor.gif)


## Core Features
- **Data Scraping:** Scrapes betting events data from multiple sources.
- **Data Normalization:** Normalizes the scraped data for consistency.
- **Telegram Bot Integration:** Provides functionalities to interact with the data via a Telegram bot.
- **Environment Configuration:** Utilizes environment variables for configuration management.
- **Helper Functions:** Includes various helper functions to support the main functionalities.

![](prematch_bettor2.gif)

## Technologies Used
- **Python:** The primary programming language used for the project.
- **Requests:** For making HTTP requests to scrape data.
- **BeautifulSoup:** For parsing HTML and extracting data.
- **pyTelegramBotAPI:** For integrating with Telegram.
- **python-dotenv:** For managing environment variables.
- **levenshtein-distance:** For calculating the Levenshtein distance between strings.

![Python](https://img.shields.io/badge/python-%233776AB.svg?style=for-the-badge&logo=python&logoColor=white)
![Requests](https://img.shields.io/badge/requests-%2300C7B7.svg?style=for-the-badge&logo=python&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/beautifulsoup-%23003B57.svg?style=for-the-badge&logo=python&logoColor=white)
![pyTelegramBotAPI](https://img.shields.io/badge/pyTelegramBotAPI-%231FA2F1.svg?style=for-the-badge&logo=python&logoColor=white)
![python-dotenv](https://img.shields.io/badge/python--dotenv-%2300BFFF.svg?style=for-the-badge&logo=python&logoColor=white)
![levenshtein-distance](https://img.shields.io/badge/levenshtein--distance-%23000000.svg?style=for-the-badge&logo=python&logoColor=white)