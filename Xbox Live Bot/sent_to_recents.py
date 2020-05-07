from bots import RecentScraper, XMessenger
import json
import time
import pandas as pd

DATA_CSV = 'sent.csv'
FRIENDS_CSV = 'friends.csv'
CONFIG_FILE = 'config.json'

# create constants to login with --> use configuration file
with open(CONFIG_FILE, 'r') as config:
    # open the file
    information = json.load(config)

    # load the data into constants
    EMAIL = information['email']
    PASSWORD = information['password']
    X_AUTH_KEY = information['X-Auth']
    MAX_RECENTS = information['max_recents']
    MESSAGE = information['message']
    BLOCK_START_TIME_UTC = information['block_start_time_utc']
    BLOCK_STOP_TIME_UTC = information['block_stop_time_utc']


# create a scraper and scrape all recents
scraper = RecentScraper(EMAIL, PASSWORD)
messenger = XMessenger(EMAIL, PASSWORD, X_AUTH_KEY)

# create the driver, scrape, close the driver
scraper.create_webdriver()
scraper.login()
scraper.enter_xbox_homepage()
recents = set(scraper.get_recents(MAX_RECENTS))
scraper.close_webdriver()

# get people that have already been sent a message
old_df = pd.read_csv(DATA_CSV, header=0)
header_row = old_df.columns
removables_df = old_df[old_df['sent_time'] > BLOCK_START_TIME_UTC][old_df['sent_time'] < BLOCK_STOP_TIME_UTC]
removables = set(removables_df['gamertag'])

# remove users that are friends
friends_df = pd.read_csv(FRIENDS_CSV, header=0)
friends = set(friends_df['gamertag'])
removables = removables | friends

to_send = list(recents - removables)

# send the messages to the appropriate gamertags
for gamertag in to_send:
    messenger.send_message(gamertag, MESSAGE)
    print(f"Message sent to {gamertag}")
    time.sleep(1)


# add the sent data to the dataframe
send_time = time.time()
data = [[recipient, MESSAGE, send_time] for recipient in to_send]
appendable_df = pd.DataFrame(data, columns=header_row)
output_df = old_df.append(appendable_df, ignore_index=True)
output_df.to_csv(DATA_CSV, index=False)


'''
NOTES
- make a way to update the stop time to the current time
- create a tools file for creating classes to manage files easily
'''
