import os

try:
    import pandas
except ImportError:
    os.system('python3 -m pip install pandas')

try:
    import datetime
except ImportError:
    os.system('python3 -m pip install datetime')

try:
    import yfinance
except ImportError:
    os.system('python3 -m pip install yfinance')


# check if it all works
import pandas
import datetime
import yfinance

print('Everything has been installed! You can run extend_xl.py now!')
