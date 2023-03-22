<a href="https://codeclimate.com/github/iwatkot/paysysmirbot/maintainability"><img src="https://api.codeclimate.com/v1/badges/53242d851173a196c116/maintainability" /></a>

## How and why
An example of this bot runs in [@paysysmirbot](https://t.me/paysysmirbot). This telegram bot uses beautifulsoup4 to scrap data from [Payment System MIR official website](https://mironline.ru/support/list/kursy_mir/). It handles exchange-rated data (directly scraping it from the website and calculates the inverted exchange rate 1 / x). Script packing data from the website to a simple JSON file along with some metadata. As long as exchange rates change only once per day, the bot checks the date in JSON metadata at first. If the data was recorded today, it will use without requesting new data from the website. The script will request new data if it wouldn't find the JSON file or if the file will be outdated. The script stores JSON data files in `data` directory.

## Available commands
`/start` - welcomes user, sends exchange rates and tips about other two commands\
`/rates` - whenever you want to know the exchange rates\

## Good to know
The bot uses `User-Agent` from the external file, which doesn't appear in the repo. Remember to put the correct User-Agent to the script (with `decouple` or manually), otherwise, your request to the website will be denied.

## Logging
Since the website might try to block scraping (or if the structure of the page will change), the bot has simple logging implemented. Logs are stored in the `logs` directory. All logs are stored in the file `main_log.txt`. It contains both: information about the scraping script - whenever the JSON file was loaded or when scripts made a new request to the website and dump data to the file, and information about all user interactions with the bot (who and when entered different commands).

## Templates
The bot uses message templates, which storing in the JSON file in `templates` directory and accessing to the messages by its key in the file.

## Changelog
**2023/03/22** Removed /notify command. Removed the number of currencies check in script.py.<br>
**2023/01/12** Added logging to `stdout`, should be working with `docker logs` too.<br>
**2023/01/12** Added `aiocron` for scheduled data update (every three hours) to avoid situations when the data file was generated today, but it contains old data, due to slow exchange rate updates on the source website.