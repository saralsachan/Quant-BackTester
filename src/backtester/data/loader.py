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
    
    # Make column names lowercase so we don't have to type "Close" everywhere
    data.columns = [name.lower() for name in data.columns]
    return data

"""yf.download: returns a pandas DataFrame with daily prices and volume
   auto_adjust = True : makes adjusted close happen
   progress = False : just hides the progress bar, cleaner output"""