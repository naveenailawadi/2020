from binance.client import Client
import pandas as pd
import ta  # keep this here --> it is how you will get technical indicators for the dataset


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
    def __init__(self, raw_csv, build_csv):
        self.headers = ["Timestamp", "Open", "High", "Low", "Close", "Volume_BTC"]
        self.build_csv = build_csv
        self.raw_csv = raw_csv
        self.client = Client()

    # this function automatically adds everything
    def add(self, records):
        # get the new records into a new dataframe
        formatted_records = [[record.timestamp, record.open, record.high,
                              record.low, record.close, record.volume] for record in records]

        new_df = pd.DataFrame(formatted_records, columns=self.headers)

        # add the new df to the old one
        raw_df = pd.DataFrame(self.raw_csv, columns=self.headers)
        raw_df.append(new_df, ignore_index=True).drop_duplicates(inplace=True)
        raw_df.to_csv(self.raw_csv)

        # rewrite the old df with technicals
        build_df = self.get_technicals(raw_df)
        build_df.to_csv(self.build_csv)

    def get_technicals(self, raw_df):
        build_df = ta.utils.dropna(raw_df)
        build_df = ta.add_all_ta_features(raw_df, open="Open", high="High", low="Low",
                                          close="Close", volume="Volume_BTC")

    def build_set_on_timeframe(self, ticker, timeframe):
        klines = self.client.get_historical_klines(ticker, Client.KLINE_INTERVAL_1MINUTE, timeframe)
        records = [Record(kline) for kline in klines]

        self.add(records)
