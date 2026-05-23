"""ML-based stock ranker using logistic regression."""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler


FEATURE_COLS = ["mom_12m", "reversal_1m", "mom_12_1", "vol_6m", "mom_3m"]


def train_and_predict(train_data, test_data):
    """Train logistic regression on train_data, predict probabilities on test_data.
    
    train_data: DataFrame of features + target for the training period.
    test_data: DataFrame of features for the test period.
    
    Returns test_data with an added 'predicted_prob' column.
    """
    # Separate features and target
    X_train = train_data[FEATURE_COLS]
    y_train = train_data["target"]
    X_test = test_data[FEATURE_COLS]
    """It looks weird to not add train_test_split
    The issue is that this split randomly shuffles the data, which is the problem with time-series data
    Instead we had already split the data according to the dates in features file"""
    
    # Standardize features (subtract mean, divide by std)
    # Important: scaler is fit on TRAIN data only, then applied to both
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train logistic regression
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_scaled, y_train)
    
    # Predict probability of class 1 (beat median)
    predictions = model.predict_proba(X_test_scaled)[:, 1]
    
    # Attach predictions to test data
    result = test_data.copy()
    result["predicted_prob"] = predictions
    
    return result, model






def ml_momentum_positions(features_with_target, prices, train_years=5, top_n=5):
    """Generate ML-based monthly positions using walk-forward training.
    
    features_with_target: long-format DataFrame from compute_target().
    prices: original price DataFrame (used to define position dates).
    train_years: years of history for training each model.
    top_n: number of stocks to hold each month.
    
    Returns a DataFrame of daily positions (one column per stock).
    """
    # Get sorted unique month-end dates
    all_months = sorted(features_with_target["date"].unique())
    
    # Build empty positions DataFrame
    monthly_positions = pd.DataFrame(
        0.0, 
        index=pd.DatetimeIndex(all_months), 
        columns=prices.columns,
    )
    
    train_months = train_years * 12
    
    # Walk forward: for each month after the warmup, train and predict
    for i, current_month in enumerate(all_months):
        if i < train_months:
            continue  # Not enough history yet
        
        # Training data: the previous train_months months
        train_start = all_months[i - train_months]
        train_end = all_months[i - 1]
        train_data = features_with_target[
            (features_with_target["date"] >= train_start) &
            (features_with_target["date"] <= train_end)
        ]
        
        # Test data: just this month
        test_data = features_with_target[features_with_target["date"] == current_month]
        
        if len(test_data) == 0 or len(train_data) == 0:
            continue
        
        # Train and predict
        result, _ = train_and_predict(train_data, test_data)
        
        # Pick top N stocks
        top_stocks = result.nlargest(top_n, "predicted_prob")["ticker"].tolist()
        
        # Set positions for those stocks to 1/N
        for ticker in top_stocks:
            if ticker in monthly_positions.columns:
                monthly_positions.loc[current_month, ticker] = 1.0 / top_n
    
    # Expand to daily and forward-fill
    daily_positions = monthly_positions.reindex(prices.index, method="ffill").fillna(0)
    
    return daily_positions