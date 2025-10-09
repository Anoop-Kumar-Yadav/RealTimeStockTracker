import os
import sys
from logger_config import logger
from api_fetcher import fetch_stock_data
from indicator_calculator import add_indicators
from db_manager import DBManager

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from setup.setup_db import createDB

def main():
    logger.info("Starting Stock Tracker Application")
    createDB()

    db = DBManager()

    # Fetch only active symbols from watchlist
    active_watchlist = db.get_active_watchlist()
    if not active_watchlist:
        logger.info("No active symbols in watchlist. Exiting.")
        db.close()
        return

    logger.info(f"Active watchlist: {active_watchlist}")

    for ticker in active_watchlist:
        logger.info(f"Processing {ticker}")

        try:
            df = fetch_stock_data(ticker)
            if df.empty:
                logger.warning(f"No data fetched for {ticker}")
                continue

            df = add_indicators(df)
            db.insert_stock_data(df, ticker)
            logger.info(f"Data processed and inserted/updated for {ticker}")

        except Exception as e:
            logger.error(f"Failed to process {ticker}: {e}")

    db.close()
    logger.info("Stock Tracker Application finished")

if __name__ == "__main__":
    main()
