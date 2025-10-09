import pandas as pd

def calculate_sma(df,window=14):

    sma = df['close_price'].rolling(window=window).mean()
    return sma

def calculate_rsi(df,window=14):

    delta = df['close_price'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

def add_indicators(df,sma_window=14,rsi_window=14):
    df['sma'] = calculate_sma(df, sma_window)
    df['rsi'] = calculate_rsi(df, rsi_window)
    return df