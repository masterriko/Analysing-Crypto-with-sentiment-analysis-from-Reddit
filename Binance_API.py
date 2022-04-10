import pandas as pd
from binance.client import Client
import datetime
import binance

client = binance.Client()

start_date = datetime.datetime.strptime("5 Oct 2021", "%d %b %Y")
today = datetime.datetime.today()

def binanceBarExtractor(symbol):
    """Get's hourly bitcoin price in tether and unix timestamp from Binance API"""
    print('working...')
    filename = "{}_HourlyBars.csv".format(symbol)

    klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1HOUR, start_date.strftime("%d %b %Y %H:%M:%S"), today.strftime("%d %b %Y %H:%M:%S"), 1000)
    data = pd.DataFrame(klines, columns = ["timestamp", "open", "high", "low", "close", "volume", "close_time", "quote_av", "trades", "tb_base_av", "tb_quote_av", "ignore" ])
    data.set_index('timestamp', inplace=True)
    data.to_csv(filename, sep = ";")
    print("finished!")


binanceBarExtractor("BTCUSDT")
