"""Walk_forward is not a strategy or metric - it is a technique of evaluating strategies on out of sample data"""


import pandas as pd


def walk_forward_splits(dates, train_years=5, test_years=1):
    """Generate (train_dates, test_dates) tuples for walk-forward analysis.
    
    dates: a DatetimeIndex of all available trading dates.
    train_years: how many years of history each training/warmup window contains.
    test_years: how many years of test data per fold (usually 1).
    
    Yields tuples of (train_window, test_window) as DatetimeIndex slices.
    """
    start = dates.min()
    end = dates.max()
    
    # Convert years to days (rough — uses 365.25 to handle leap years on average)
    #Timdedelta - pandas way to represent a span of time
    train_days = pd.Timedelta(days=int(train_years * 365.25))
    test_days = pd.Timedelta(days=int(test_years * 365.25))
    
    fold_start = start
    while (fold_start + train_days + test_days <= end):
        train_end = fold_start + train_days
        test_end = train_end + test_days
        
        train_window = dates[(dates >= fold_start) & (dates < train_end)]
        test_window = dates[(dates >= train_end) & (dates < test_end)]
        
        #yield make the function a generator - the function does not stop after  returning a value, it stops only when loop terminates
        yield train_window, test_window
        
        fold_start = fold_start + test_days  # Roll forward by one test period

