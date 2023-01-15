<a href="https://codeclimate.com/github/iwatkot/paysysmirbot/maintainability"><img src="https://api.codeclimate.com/v1/badges/53242d851173a196c116/maintainability" /></a>

## How and why
The example of this bot runs in [@paysysmirbot](https://t.me/paysysmirbot). This telegram bot uses beautifulsoup4 to scrap data from [Payment System MIR official website](https://mironline.ru/support/list/kursy_mir/). It handles with exhchange rated data (directrly scraping it from the website and calculates the inverted exchange rate 1 / x). Script packing data from the website to a simple JSON file along with some metadata. As long as exchange rates changing only once per day, the bot checking the date in JSON metadata at first. If the data was recorded today, it will use it without requesting new data from the website. Script will request new data if the it wouldn't find the JSON file or if the file will be outdated. The script stores JSON data file in `data` directory.

## Available commands
`/start` - welcomes user, sends exchange rates and tips about other two commands\
`/rates` - whenever you want to know the exhcange rates\
`/notify` - aftet enetering this command the bot will send you exhchange rates every 24 hours\

## Good to know
The bot using `User-Agent` from the external file, which is obviously doesn't appear in the repo. Remember to put the correct User-Agent to the script (with `decouple` or manually), otherwise your request to the website will be denied.

## Logging
Since the website might try to block scraping (or if the structure of the page will change), the bot has simple logging implemented. Logs are stored in the `logs` directory. All logs are stored in the file `main_log.txt`. It contains both: information about scraping script - whenever the JSON file was loaded or when scripts made a new request to the website and dump data to the file, and information about all user ineractions with bot (who and when entered different commands).

## Templates
The bot using message templates, which storing in the JSON file in `templates` directory and accessing to the messages by it's key in the file.

## Changelog
**2023/01/12** Added logging to `stdout`, should be working with `docker logs` too.<br>
**2023/01/12** Added `aiocron` for scheduled data update (every three hours) to avoid situations when the data file was generated today, but it contains old data, due to slow exchange rates updates on the source website.