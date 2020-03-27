from bs4 import BeautifulSoup as bs
from yahoo_fin import stock_info as si
import requests


# create a class with all the company's information
'''
INFORMATION to scrape for
- name
- market cap
- price per share
- EV/(Revenue TTM)
- EV/(EBIT TTM)
    - calculate manually --> net income + interest + taxes
- EV/(EBITDA TTM)
- EV/(FCF TTM)
    - calculate manually --> EV/(Unlevered Free cash flow)
'''


class Company:
    def __init__(self, ticker):
        self.ticker = ticker
        self.get_links()
        self.scrape_general()
        self.calc_ebit()
        self.get_primary_data()

    # get the links that will be used for information
    def get_links(self):
        self.stat_link = f'https://finance.yahoo.com/quote/{self.ticker}/key-statistics?p={self.ticker}'
        self.finc_link = f'https://finance.yahoo.com/quote/{self.ticker}/financials?p={self.ticker}'
        self.guru_links = [
            f'https://www.gurufocus.com/term/Preferred+Stock/{self.ticker}/Preferred-Stock',
            f'https://www.gurufocus.com/term/Minority_interest/{self.ticker}/Minority-Interest',
            f'https://www.gurufocus.com/term/LongTermDebt/{self.ticker}/Long-Term-Debt',
            f'https://www.gurufocus.com/term/ShortTermDebt_without_lease/{self.ticker}/Short-Term-Debt',
            f'https://www.gurufocus.com/term/CashAndCashEquivalents/{self.ticker}/Cash-And-Cash-Equivalents',
            f'https://www.gurufocus.com/term/BS_share/{self.ticker}/Shares-Outstanding-(EOP'
        ]

    # scrape the general information
    def scrape_general(self):
        raw = requests.get(self.stat_link).text
        soup = bs(raw, 'html.parser')

        # get general info
        self.name = soup.find('h1').text.split(self.ticker)[1][3:]

        # all tables of information
        tables = soup.find_all('tbody')

        # get market cap
        valuation_measures = tables[0]
        valuation_metrics = valuation_measures.find_all('tr')
        market_cap_str = valuation_metrics[0].find_all('td')[1].text
        self.market_cap = string_to_num(market_cap_str)

        # get EV
        self.enterprise_value = string_to_num(valuation_metrics[1].find_all('td')[1].text)

        # get price per share
        self.price_per_share = round(float(si.get_live_price(self.ticker)), 2)

        # get EV/(Revenue TTM)
        self.ev_to_revenue = valuation_metrics[-2].find_all('td')[1].text

        # get EV/(EBITDA TTM)
        self.ev_to_ebitda = valuation_metrics[-1].find_all('td')[1].text

        # get EV/(FCF TTM)
        cash_flow_statement = tables[9]
        levered_cash_flow = string_to_num(cash_flow_statement.find_all('tr')[-1].find_all('td')[1].text)
        try:
            self.ev_to_fcf = float(levered_cash_flow) / float(self.enterprise_value)
        except ValueError:
            self.ev_to_fcf = '-'

    def calc_ebit(self):
        raw = requests.get(self.finc_link).text
        soup = bs(raw, 'html.parser')
        income_statement_spans = soup.find_all('span')

        # net income
        count = 0
        for span in income_statement_spans:
            found_net_income = False
            found_interest = False
            found_taxes = False
            if not found_net_income:
                if "Net Income" in span.text:
                    net_income = float(income_statement_spans[count + 1].text)
                    found_net_income = True

            if not found_interest:
                if "Interest Expense" in span.text:
                    try:
                        interest = float(income_statement_spans[count + 1].text)
                    except ValueError:
                        added = 1
                        while True:
                            try:
                                interest = float(income_statement_spans[count + added].text)
                                found_interest = True
                            except ValueError:
                                added += 1
                            if 'total' in span.text.lower():
                                return '-'

            if not found_taxes:
                if "Income Tax Expense" in span.text:
                    taxes = float(income_statement_spans[count + 1].text)
                    found_taxes = True

            if found_net_income and found_interest and found_taxes:
                break
            # add one for each iteration
            count += 1

        # get ebit info
        self.ebit = net_income + interest + taxes

        # calculate EV/EBIT
        self.ev_to_ebit = self.enterprise_value / self.ebit

    # get preferred stock
    def get_guru_data(self, guru_link):
        raw = requests.get(guru_link).text
        soup = bs(raw, 'html.parser')
        font_info = {"style": "font-size: 24px; font-weight: 700; color: #337ab7"}
        tag = soup.find('font', font_info).text

        # clean up the tag text
        ends = tag.split('$')[1].split(' ')
        value = ends[0]  # preferred stock value
        multiplier = ends[1][:1]
        value += multiplier
        guru_data = string_to_num(value)
        return guru_data

    def get_primary_data(self):
        self.preferred_stock = self.get_guru_data(self.guru_links[0])
        self.minority_interest = self.get_guru_data(self.guru_links[1])

        long_term_debt = self.get_guru_data(self.guru_links[2])
        short_term_debt = self.get_guru_data(self.guru_link[3])
        self.total_debt = long_term_debt + short_term_debt

        self.cash = self.get_guru_data(self.guru_links[4])
        self.shares_outstanding = self.get_guru_data(self.guru_links[5])
        self.revenue = (1 / self.ev_to_revenue) * self.enterprise_value
        self.ebitda = (1 / self.ev_to_ebitda) * self.enterprise_value
        self.fcf = (1 / self.ev_to_fcf) * self.enterprise_value


# convert strings with letters denoting thousands, millions, or billions into regular floats
def string_to_num(num_string):
    # make it easier to scan
    num_string = num_string.lower()

    # convert to correct value
    if 'b' in num_string:
        num = float(num_string.split('b')[0])
        num *= 1000000000.0

    elif 'm' in num_string:
        num = float(num_string.split('m')[0])
        num *= 1000000.0

    elif ('k' in num_string) or ('t' in num_string):
        num = float(num_string.split('k')[0])
        num *= 1000.0
    else:
        try:
            num = float(num_string)
        except ValueError:
            num = "-"

    return num

# create a function to turn values into accounting format


def af(num):
    num = str(num)
    accounting_formatted_number = '${:,.2f}'.format(num)
    return accounting_formatted_number


# create a function to find the average of a list
def average(my_list):
    average = sum(my_list) / len(my_list)
    return average


# create a function to find the median of a list
def median(my_list):
    length = len(my_list)
    my_list.sort()

    if length % 2 == 0:
        median1 = my_list[length // 2]
        median2 = my_list[length // 2 - 1]
        median = (median1 + median2) / 2
    else:
        median = my_list[length // 2]

    return median
