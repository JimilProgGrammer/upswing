# Import Section
import datetime
import pandas as pd
from pymongo import MongoClient
from pandas_datareader import data, wb

def yahoo_finance(symbol, start_date):
    # Pulling data from Yahoo Finance and formmatting it in our DB format
    df = data.DataReader(symbol +".NS" , 'yahoo', start=start_date)
    df = df.reset_index()
    df = df.rename(columns = {'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Date': 'timestamp', 'Volume': 'volume'})
    df = df[["open", "high", "low", "close", "timestamp", "volume"]]
    return df