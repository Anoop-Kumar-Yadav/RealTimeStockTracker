import yfinance as yf
import pandas as pd
from config import USE_YFINANACE, ALPHA_VANTAGE_KEY
from logger_config import logger

def fetch_stock_data(symbol, period="1mo", interval="1d"):
    try:
        if USE_YFINANACE:
            logger.info(f"Fetching data for {symbol} using yfinance...")
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period, interval=interval)

            if df.empty:
                logger.warning(f"No data fetched for {symbol}")
                return pd.DataFrame()

            df = df.reset_index()
            df = df.rename(columns={
                "Date": "date",
                "Open": "open_price",
                "High": "high_price",
                "Low": "low_price",
                "Close": "close_price",
                "Volume": "volume"
            })
            df = df[["date", "open_price", "high_price", "low_price", "close_price", "volume"]]

            logger.info(f"Fetched {len(df)} rows for {symbol}")
            return df
        else:
            raise NotImplementedError("Alpha Vantage API integration coming soon.")

    except Exception as e:
        logger.error(f"Error fetching data for {symbol}: {e}")
        return pd.DataFrame()
