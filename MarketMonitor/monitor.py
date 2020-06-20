from forex_python.converter import CurrencyRates, CurrencyCodes
from bs4 import BeautifulSoup as bs
import requests


class ForexMonitor(CurrencyRates, CurrencyCodes):
    # create a function to compare based on a set forx
    def usd_to(self, symbol):
        # get rate
        rate = self.convert('USD', symbol, 1)

        usd_symbol = self.get_symbol('USD')
        other_symbol = self.get_symbol(symbol)
        return f"{usd_symbol}1 : {other_symbol}{rate}"


class CommodityMonitor:
    # get the price of oil in dollars
    def get_wti_price(self):
        # make a soup object --> get the price info
        raw = requests.get('https://oilprice.com/oil-price-charts')
        soup = bs(raw.text, 'html.parser')

        wti_price = soup.find('h2')[0].text

        return wti_price


'''
NOTES
- this monitors the forex and oil markets and pushes data via telegram
'''
