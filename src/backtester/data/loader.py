import yfinance as yf
import pandas as pd;

def load_ticker(ticker, st, en):
    """ticker: stock symbol-  eg: RELIANCE.NS
       st: start date as string
       en: end date as string""" 
       
    data = yf.download(ticker, start = st, end = en, auto_adjust = True, progress = False)
    # If yfinance returned nested columns, flatten them
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.droplevel(1)
    
    return data

"""yf.download: returns a pandas DataFrame with OHLCV data for each day
   auto_adjust = True : makes adjusted close happen
   progress = False : just hides the progress bar, cleaner output"""
   
   
#loading multiple tickers   
def load_multiple_tickers(tickers , st, en):
    #download data for a list of stocks
    #tickers is a list
    """return a dictionary: {ticker_name: DataFrame containing OHLCV data for each day}"""
    
    result = {} 
    """we call our prev function for each item of tickers list"""
    for ticker in tickers:
       print(f"Loading {ticker} ...")
       df = load_ticker(ticker, st, en)
       result[ticker] = df
    
    return result;    