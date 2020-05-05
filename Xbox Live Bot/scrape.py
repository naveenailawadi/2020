from bots import RecentScraper
import json

# create constants to login with --> use configuration file
with open('config.json', 'r') as config:
    # open the file
    information = json.load(config)

    # load the data into constants
    EMAIL = information['email']
    PASSWORD = information['password']
    MAX_RECENTS = information['max_recents']

print(information)


# create a scraper and scrape all
recents = RecentScraper(EMAIL, PASSWORD).scrape(MAX_RECENTS)


for recent in recents:
    print(recent)
