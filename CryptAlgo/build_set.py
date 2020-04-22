from DataMiner import Miner
import time
from datetime import datetime as dt
from multiprocessing import Pool
import os

TICKERS = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'LTCUSDT']
TIMEFRAME = '1 hour ago UTC'
PROCESSES = 2 * os.cpu_count()

# reassign the proceesses to the number of tickers if it exceeds it
if len(TICKERS) < PROCESSES:
    PROCESSES = len(TICKERS)


# build our set on current data
def inf_builder(ticker):
    miner = Miner(f"data/{ticker}_raw_4_22_20.csv")
    while True:
        miner.build_set_on_timeframe(ticker, TIMEFRAME)
        size = miner.raw_size()
        now = dt.now()

        print(f"{now.time()}  \n{ticker} records: {size}   \nDays: {round(size / 1440, 2)}    \n")

        time.sleep(3300)


# get the data
with Pool(processes=PROCESSES) as pool:
    pool.map(inf_builder, TICKERS, chunksize=1)
