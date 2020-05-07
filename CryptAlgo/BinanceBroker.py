from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceWithdrawException
from binance.enums import *

# initialize api
KEY = 'nqoE8NVAPkEVX26miyXMB3AEtxAfMWY1QZbKusWxv5utKvIvg542c8z3CE5FhK52'
SECRET = 'RKl6AOL0Vr5P2rCnpNmaTggk98P8yv3YO3pDtgCALrp8FK26RlDxMW4PWNt8O8mG'
client = Client(KEY, SECRET)

# load constants
SYMBOL_TYPE_SPOT = 'SPOT'

ORDER_STATUS_NEW = 'NEW'
ORDER_STATUS_PARTIALLY_FILLED = 'PARTIALLY_FILLED'
ORDER_STATUS_FILLED = 'FILLED'
ORDER_STATUS_CANCELED = 'CANCELED'
ORDER_STATUS_PENDING_CANCEL = 'PENDING_CANCEL'
ORDER_STATUS_REJECTED = 'REJECTED'
ORDER_STATUS_EXPIRED = 'EXPIRED'

KLINE_INTERVAL_1MINUTE = '1m'
KLINE_INTERVAL_3MINUTE = '3m'
KLINE_INTERVAL_5MINUTE = '5m'
KLINE_INTERVAL_15MINUTE = '15m'
KLINE_INTERVAL_30MINUTE = '30m'
KLINE_INTERVAL_1HOUR = '1h'
KLINE_INTERVAL_2HOUR = '2h'
KLINE_INTERVAL_4HOUR = '4h'
KLINE_INTERVAL_6HOUR = '6h'
KLINE_INTERVAL_8HOUR = '8h'
KLINE_INTERVAL_12HOUR = '12h'
KLINE_INTERVAL_1DAY = '1d'
KLINE_INTERVAL_3DAY = '3d'
KLINE_INTERVAL_1WEEK = '1w'
KLINE_INTERVAL_1MONTH = '1M'

SIDE_BUY = 'BUY'
SIDE_SELL = 'SELL'

ORDER_TYPE_LIMIT = 'LIMIT'
ORDER_TYPE_MARKET = 'MARKET'
ORDER_TYPE_STOP_LOSS = 'STOP_LOSS'
ORDER_TYPE_STOP_LOSS_LIMIT = 'STOP_LOSS_LIMIT'
ORDER_TYPE_TAKE_PROFIT = 'TAKE_PROFIT'
ORDER_TYPE_TAKE_PROFIT_LIMIT = 'TAKE_PROFIT_LIMIT'
ORDER_TYPE_LIMIT_MAKER = 'LIMIT_MAKER'

TIME_IN_FORCE_GTC = 'GTC'
TIME_IN_FORCE_IOC = 'IOC'
TIME_IN_FORCE_FOK = 'FOK'

ORDER_RESP_TYPE_ACK = 'ACK'
ORDER_RESP_TYPE_RESULT = 'RESULT'
ORDER_RESP_TYPE_FULL = 'FULL'

# For accessing the data returned by Client.aggregate_trades().
AGG_ID = 'a'
AGG_PRICE = 'p'
AGG_QUANTITY = 'q'
AGG_FIRST_TRADE_ID = 'f'
AGG_LAST_TRADE_ID = 'l'
AGG_TIME = 'T'
AGG_BUYER_MAKES = 'm'
AGG_BEST_MATCH = 'M'


# create a class to load into the algorithm
class TradeSlice:
    def __init__(dict_info):
        self.price = price
        self.volume = volume
        self.time = time
        self.vwap = VWAP


# run class
symbol = 'BTCUSDT'

'''
NOTES
- inputs: price, time, VWAP
- ALWAYS check for 429 errors (warning for ban) --> rest for an hour
- bitcoin ticker: BTCUSDT

EXAMPLE KLINE RESPONSE
[1581029400000,  # timestamp (miliseconds)
'9715.01000000', # open
'9719.31000000', # high
'9715.01000000', # low
'9715.36000000', # close
'40.35176000', # volume
1581029459999, # close time
'392062.02410586', # quote asset volume
408, # number of trades
'14.41288300', ' # taker buy base asset volume --> amount being bought
140056.44775208', # taker by quote asset volume --> amount being sold
'0']

background-image: url("https://i1.sndcdn.com/artworks-000369285036-qrl6uu-t500x500.jpg"); width: 100%; height: 100%; opacity: 1;

SOURCES
- https://towardsdatascience.com/creating-bitcoin-trading-bots-that-dont-lose-money-2e7165fb0b29

'''
