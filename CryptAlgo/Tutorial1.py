import datetime
from time import sleep
from binance.client import Client

# initialize api
KEY = 'nqoE8NVAPkEVX26miyXMB3AEtxAfMWY1QZbKusWxv5utKvIvg542c8z3CE5FhK52'
SECRET = 'RKl6AOL0Vr5P2rCnpNmaTggk98P8yv3YO3pDtgCALrp8FK26RlDxMW4PWNt8O8mG'
client = Client(KEY, SECRET)

# input symbols and quantity
symbol = 'BTCUSDT'
quantity = '0.05'

order = False

while not order:
    BTC = client.get_historical_klines(symbol=symbol, interval='1m', start_str="1 minute ago UTC")
    print(BTC)
    break
