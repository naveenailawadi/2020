from forex_python.converter import CurrencyRates, CurrencyCodes
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import time


class ForexMonitor(CurrencyRates, CurrencyCodes):
    # create a function to compare based on a set forx
    def usd_to(self, symbol):
        # get rate
        rate = round(self.get_rate('USD', symbol), 2)

        other_symbol = self.get_symbol(symbol)
        return f"$1 : {other_symbol}{rate}"


class CommodityMonitor:
    # get the price of oil in dollars
    def get_wti_price(self):
        # use selenium (better for interacting with JS)
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)
        driver.get('https://oilprice.com/oil-price-charts')
        time.sleep(2)

        # get the oil price
        wti_price_raw = driver.find_element_by_xpath('//tr[@data-spreadsheet="Crude Oil WTI"]//td[@class="last_price"]').text
        wti_price = f"${wti_price_raw} (per barrel)"
        driver.quit()

        return wti_price


'''
NOTES
- this monitors the forex and oil markets and pushes data via telegram
'''
