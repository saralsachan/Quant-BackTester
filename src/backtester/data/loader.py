import yfinance as yf
import pandas as pd;

def load_ticker(ticker, st, en):
    """ticker: stock symbol-  eg: RELIANCE.NS
       st: start date as string
       en: end date as string""" 
       
    data = yf.download(ticker, start = st, end = en, auto_adjust = True, progress = False)
    # If yfinance returned nested columns, flatten them
    
    
    if data.empty:
        raise ValueError(f"No data returned for {ticker}")

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.droplevel(1)
    
    return data

"""yf.download: returns a pandas DataFrame with OHLCV data for each day
   auto_adjust = True : makes adjusted close happen
   progress = False : just hides the progress bar, cleaner output"""
   
 
import os

def load_ticker_with_cache(ticker, start, end):
    """Load a ticker, using cached data only if it covers the requested range."""
    
    # Build the cache path (absolute, based on this file's location)
    this_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(this_file))))
    cache_folder = os.path.join(project_root, "data", "raw")
    os.makedirs(cache_folder, exist_ok=True)
    
    safe_name = ticker.replace(".", "_")
    cache_file = os.path.join(cache_folder, f"{safe_name}.parquet")
    
    requested_start = pd.Timestamp(start)
    requested_end = pd.Timestamp(end)
    
    # If cache file exists, check if it actually covers what we need
    if os.path.exists(cache_file):
        cached = pd.read_parquet(cache_file)
        
        if len(cached) > 0:
            cached_start = cached.index.min()
            cached_end = cached.index.max()
            
            # Cache is usable if it spans the requested range
            covers_start = cached_start <= requested_start
            covers_end = cached_end >= requested_end
            
            if covers_start and covers_end:
                print(f"Loading {ticker} from cache ({cached_start.date()} to {cached_end.date()})")
                return cached.loc[start:end]
            else:
                print(f"Cache for {ticker} doesn't cover requested range:")
                print(f"  Cached:    {cached_start.date()} to {cached_end.date()}")
                print(f"  Requested: {requested_start.date()} to {requested_end.date()}")
                print(f"  Re-downloading...")
    
    # Download fresh — and download a buffer beyond the request, so future requests
    # for slightly different ranges can still use the cache
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
      try:
          print(f"Loading {ticker} ...")
          df = load_ticker_with_cache(ticker, st, en) #updated load_ticker with cache function
          result[ticker] = df
      except ValueError as e:
          print(f"Skipping {ticker}: {e}")    
    
    return result;    
     
def check_data_quality(prices):
    """"Print a summary of how clean data is"""
    
    print(f"Shape: {prices.shape}")     
    print(f"Date Range: {prices.index.min().date()} to {prices.index.max().date()}")
    
    total_missing = prices.isna().sum().sum()
    total_cells = prices.size #prices.size — total number of cells (rows × columns). Used to compute the percentage of missing values.
    print(f"Missing values: {total_missing} ({total_missing / total_cells:.2%})")
    
    empty_stocks = prices.columns[prices.isna().all()]
    print(f"Stocks with no data: {len(empty_stocks)}")
    if len(empty_stocks) > 0:
        print(f"  → {list(empty_stocks)}")
    
    non_positive = (prices <= 0).sum().sum()
    print(f"Non-positive prices: {non_positive}")
    
    duplicates = prices.index.duplicated().sum()
    print(f"Duplicate dates: {duplicates}")