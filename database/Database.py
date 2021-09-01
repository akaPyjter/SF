from datetime import datetime

from data_requests.CryptoRequests import get_crypto_values, change_candles_to_candle_objects



class Database:
    def __init__(self):
        #   {{crypto_currency_symbol:{resolution:{fiat:[]}}}}
        self.main_container = {}

    def add_to_data_base(self, crypto_currency_symbol, fiat_symbol):
        self.main_container[crypto_currency_symbol] = {"1": {}, "5": {}, "15": {}, "30": {}, "60": {}, "D": {}, "W": {},
                                                       "M": {}}
        for resolution in self.main_container[crypto_currency_symbol]:
            self.main_container[crypto_currency_symbol][resolution] = {fiat_symbol: []}
            candles_json = get_crypto_values(f"{crypto_currency_symbol.lower()}{fiat_symbol.lower()}", resolution, "1/01/2017", "1/09/2021")
            candle_objects = change_candles_to_candle_objects(candles_json)
            for candle in candle_objects:
                self.main_container[crypto_currency_symbol][resolution][fiat_symbol].append(candle)


    def update_candles_on_currency(self, crypto_currency_symbol):
        latest_date_dict = self.get_latest_dates(crypto_currency_symbol)
        if latest_date_dict is None or len(latest_date_dict) == 0:
            return
        for resolution in latest_date_dict:
            for fiat in latest_date_dict[resolution]:
                candles_json = get_crypto_values(crypto_currency_symbol, resolution, latest_date_dict[resolution][fiat],
                                                 datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                candle_objects = change_candles_to_candle_objects(candles_json)
                for candle in candle_objects:
                    self.main_container[crypto_currency_symbol][resolution][fiat].append(candle)

    def get_latest_dates(self, crypto_currency_symbol):
        symbol_data = self.main_container[crypto_currency_symbol]
        latest_date_dict = {}
        if len(symbol_data) > 0:
            for resolution in symbol_data:
                if len(symbol_data[resolution]) > 1:
                    for fiat, candle in symbol_data[resolution].items():
                        latest_date_dict[resolution] = {fiat: candle.time}
                    return latest_date_dict
        return
