from monitor import ForexMonitor, CommodityMonitor
from TelegramBot import Messenger
from datetime import datetime as dt
from secrets import *
import schedule
import time


# create the classes as constants
MESSENGER = Messenger(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)
FOREX_MONITOR = ForexMonitor()
COMMODITY_MONITOR = CommodityMonitor()

# create lists of the symbols
FOREX_SYMBOLS = ['EUR', 'CNY']
SEND_TIME = '10:00'


# create a function that gets all the prices and sends them
def send():
    # get the current date
    today = dt.now()
    date = f"{today.month}/{today.day}/{today.year} ({today.hour}:{str(today.minute).zfill(2)})"

    # get the current forex prices
    forex_rates = [FOREX_MONITOR.usd_to(symbol) for symbol in FOREX_SYMBOLS]

    # get the oil price
    oil_price = COMMODITY_MONITOR.get_wti_price()

    information = {
        'date': date,
        'forex_rates': forex_rates,
        'oil_rates': [oil_price]
    }

    # send it with telegram
    MESSENGER.send_html(information)


# send it over and over on a schedule
if __name__ == '__main__':
    '''
    schedule.every().day.at(SEND_TIME).do(send)

    while True:
        # Checks whether a scheduled task
        # is pending to run or not
        schedule.run_pending()
        time.sleep(10)
    '''
    send()
