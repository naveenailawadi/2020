from monitor import ForexMonitor, CommodityMonitor
from TelegramBot import Messenger
from multiprocessing import Pool
from secrets import *
import schedule
import os


# create the classes as constants
MESSENGER = Messenger(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)
FOREX_MONITOR = ForexMonitor()
COMMODITY_MONITOR = CommodityMonitor()

# create a process constant
PROCESS_MAX = 2 * os.cpu_count()


# create a function that gets all the prices and sends them
def send():
    # get the current forex prices
    with Pool(PROCESS_MAX) as pool:
        forex_rates = pool.map(FOREX_MONITOR.usd_to, ['EUR', ''])
