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
   
 
import os

def load_ticker_with_cache(ticker, start, end):
    """Load a ticker, using a saved file if we've downloaded it before."""
    
    # Make sure the cache folder exists
   # Get the path to the project root, no matter where the script is called from
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    cache_folder = os.path.join(project_root, "data", "raw")
    os.makedirs(cache_folder, exist_ok=True)
    
    # Build the filename for this ticker
    # Replace dots with underscores so "RELIANCE.NS" becomes "RELIANCE_NS.parquet"
    safe_name = ticker.replace(".", "_")
    cache_file = f"{cache_folder}/{safe_name}.parquet"
    
    # If we already have it saved, just read from disk
    if os.path.exists(cache_file):
        print(f"Loading {ticker} from cache")
        return pd.read_parquet(cache_file)
    
    # Otherwise, download and save it
    print(f"Downloading {ticker}")
    df = load_ticker(ticker, start, end)
    df.to_parquet(cache_file)
    return df 
 
"""GETTING CLOSE PRICES in a single DataFrame for different stocks""" 
def get_close_prices(data_dict):
   """Take a dictionary of DataFrames and return one DataFrame with close prices.
    
    data_dict: dictionary like {"RELIANCE.NS": df, "TCS.NS": df, ...}
    
    Returns a DataFrame where each column is one stock's close price.
    """
   close_prices = {}
   for ticker,df in data_dict.items():
      close_prices[ticker] = df["Close"]
      
   return pd.DataFrame(close_prices)   
    
    
    
   
#loading multiple tickers   
def load_multiple_tickers(tickers , st, en):
    #download data for a list of stocks
    #tickers is a list
    """return a dictionary: {ticker_name: DataFrame containing OHLCV data for each day}"""
    
    result = {} 
    """we call our prev function for each item of tickers list"""
    for ticker in tickers:
       print(f"Loading {ticker} ...")
       df = load_ticker_with_cache(ticker, st, en) #updated load_ticker with cache function
       result[ticker] = df
    
    return result;    
     