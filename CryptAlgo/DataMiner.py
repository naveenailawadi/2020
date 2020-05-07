from binance.client import Client
import pandas as pd
import ta  # keep this here --> it is how you will get technical indicators for the dataset

# load constants
PERIOD = 5
LOW_PERIOD = PERIOD / 2
MEDIUM_PERIOD = PERIOD
HIGH_PERIOD = PERIOD * 2


class Record:
    # the related records are strictly for calculating intraday trading indicators
    def __init__(self, info_list):
        self.timestamp = info_list[0]
        self.open = float(info_list[1])
        self.high = float(info_list[2])
        self.low = float(info_list[3])
        self.close = float(info_list[4])
        self.volume = float(info_list[5])
        self.quote_asset_volume = float(info_list[7])
        self.number_of_trades = info_list[8]
        self.taker_buy_base_asset_volume = float(info_list[9])
        self.taker_quote_asset_volume = float(info_list[10])


# create a general mining class
class Miner:
    def __init__(self, raw_csv):
        self.headers = ["Timestamp", "Open", "High", "Low", "Close", "Volume",
                        "Quote Asset Volume", "Number of Trades", "Taker Buy Asset Volume", "Taker Quote Asset Volume"]
        self.raw_csv = raw_csv
        self.client = Client()

    # this function automatically adds everything
    def add(self, records):
        # get the new records into a new dataframe
        formatted_records = [list(record.__dict__.values()) for record in records]

        new_df = pd.DataFrame(formatted_records, columns=self.headers)

        # add the new df to the old one
        try:
            raw_df = pd.read_csv(self.raw_csv, header=0)
            raw_df = raw_df.append(new_df, ignore_index=True).drop_duplicates(keep='first', subset=['Timestamp'])
        except FileNotFoundError:
            raw_df = new_df
            print(f"{self.raw_csv} was not found. A new file has been created")

        raw_df.to_csv(self.raw_csv, columns=self.headers, index=False)

    def get_technicals(self, raw_df, build_csv):
        build_df = ta.utils.dropna(raw_df)

        # trend indicators
        build_df['SMA'] = ta.trend.SMAIndicator(close=build_df['Close'], n=PERIOD).sma_indicator()
        build_df['EMA'] = ta.trend.EMAIndicator(close=build_df['Close'], n=PERIOD).ema_indicator()
        build_df['MACD'] = ta.trend.MACD(close=build_df['Close'], n_fast=LOW_PERIOD, n_slow=HIGH_PERIOD,).macd()

        ichimoku = ta.trend.IchimokuIndicator(low=build_df['Low'], high=build_df['High'],
                                              n1=LOW_PERIOD, n2=MEDIUM_PERIOD, n3=HIGH_PERIOD)
        build_df['ICHIMOKU_A'] = ichimoku.ichimoku_a()
        build_df['ICHIMOKU_B'] = ichimoku.ichimoku_b()

        # volumen indicator
        build_df['VWAP'] = ta.volume.VolumeWeightedAveragePrice(low=build_df['Low'], high=build_df['High'],
                                                                close=build_df['Close'], volume=build_df['Volume'],
                                                                n=PERIOD).volume_weighted_average_price()

        # send the dataframe to a csv
        build_df.to_csv(build_csv, index=False)

    def build_set_on_timeframe(self, ticker, timeframe):
        # use a generator to preserve memory and overuse of cpu
        klines = self.client.get_historical_klines(ticker, Client.KLINE_INTERVAL_1MINUTE, timeframe)

        records = [Record(kline) for kline in klines]

        self.add(records)

    def raw_size(self):
        raw_df = pd.read_csv(self.raw_csv, header=0)

        size = len(raw_df)

        return size
