import pymysql  # type: ignore
import pandas as pd
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
from logger_config import logger

class DBManager:

    def __init__(self):
        try:
            self.conn = pymysql.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                cursorclass=pymysql.cursors.DictCursor  
            )
            self.cursor = self.conn.cursor()
            logger.info("DBManager connected to database")
        except Exception as e:
            logger.error(f"DBManager connection failed: {e}")

    def record_exists(self, symbol, date):
        query = "SELECT COUNT(*) as count FROM stocks WHERE symbol = %s AND date = %s"
        self.cursor.execute(query, (symbol, date))
        result = self.cursor.fetchone()
        return result["count"] > 0

    def remove_all_stock_data(self, symbol):
        """
        Remove all stock data for the given symbol from the stocks table.

        Args:
            symbol (str): Stock symbol to delete.

        Returns:
            True if deletion was successful, False otherwise.
        """
        try:
            self.cursor.execute("DELETE FROM stocks WHERE symbol = %s", (symbol,))
            self.conn.commit()
            logger.info(f"All stock data for {symbol} removed from stocks table.")
            return True
        except Exception as e:
            logger.error(f"Failed to remove stock data for {symbol}: {e}")
            self.conn.rollback()
            return False


    def insert_stock_row(self, row, symbol):
        try:
            row = row.where(pd.notnull(row), None)  

            query = """
            INSERT INTO stocks (symbol, date, open_price, high_price, low_price, close_price, volume, sma, rsi)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, (
                symbol,
                row['date'],
                row['open_price'],
                row['high_price'],
                row['low_price'],
                row['close_price'],
                row['volume'],
                row['sma'],
                row['rsi']
            ))

            self.conn.commit()
            logger.info(f"Inserted row for {symbol} on {row['date']}")

        except Exception as e:
            logger.error(f"Insert failed for {symbol} on {row['date']}: {e}")

    def update_stock_row(self, row, symbol):
        row = row.where(pd.notnull(row), None)
        query = """
        UPDATE stocks
        SET open_price = %s,
            high_price = %s,
            low_price = %s,
            close_price = %s,
            volume = %s,
            sma = %s,
            rsi = %s
        WHERE symbol = %s AND date = %s
        """
        try:
            self.cursor.execute(query, (
                row['open_price'],
                row['high_price'],
                row['low_price'],
                row['close_price'],
                row['volume'],
                row['sma'],
                row['rsi'],
                symbol,
                row['date']
            ))
            self.conn.commit()
            logger.info(f"Updated row for {symbol} on {row['date']}")
        except Exception as e:
            logger.error(f"Update failed for {symbol} on {row['date']}: {e}")

    def insert_stock_data(self, df, symbol):
        for _, row in df.iterrows():
            if self.record_exists(symbol, row['date']):
                self.update_stock_row(row, symbol)
            else:
                self.insert_stock_row(row, symbol)
        logger.info(f"Data for {symbol} inserted/updated successfully.")

    def fetch_stock_data(self, symbol, start_date=None, end_date=None):
        query = "SELECT * FROM stocks WHERE symbol = %s"
        params = [symbol]

        if start_date:
            query += " AND date >= %s"
            params.append(start_date)
        if end_date:
            query += " AND date <= %s"
            params.append(end_date)

        query += " ORDER BY date ASC"
        self.cursor.execute(query, params)
        result = self.cursor.fetchall()

        return pd.DataFrame(result)

    def fetch_watchlist(self):
        try:
            self.cursor.execute("SELECT symbol, active FROM watchlist")
            rows = self.cursor.fetchall()
            # Only return the values for symbol and active
            return [(row["symbol"], row["active"]) for row in rows]
        except Exception as e:
            logger.error(f"Error fetching watchlist: {e}")
            return []
    


    def add_to_watchlist(self, symbol):
        
        try:
            query = "INSERT IGNORE INTO watchlist (symbol) VALUES (%s)"
            self.cursor.execute(query, (symbol,))
            self.conn.commit()
            logger.info(f"Added {symbol} to watchlist.")
            return {"status" : 1}
        except Exception as e:
            logger.error(f"Error adding {symbol} to watchlist: {e}")
            self.conn.rollback()
            return {"status" : 0}

    def remove_from_watchlist(self, symbol):
        """
        Remove a symbol from the watchlist table.

        Returns:
            True if removed successfully, False otherwise.
        """
        try:
            # Check if the symbol exists
            self.cursor.execute("SELECT COUNT(*) as count FROM watchlist WHERE symbol = %s", (symbol,))
            result = self.cursor.fetchone()
            if result["count"] == 0:
                logger.warning(f"Symbol {symbol} not found in watchlist.")
                return False

            # Delete the symbol
            self.cursor.execute("DELETE FROM watchlist WHERE symbol = %s", (symbol,))
            self.conn.commit()
            self.remove_all_stock_data(symbol)
            logger.info(f"Symbol {symbol} removed from watchlist successfully.")
            return True

        except Exception as e:
            logger.error(f"Error removing {symbol} from watchlist: {e}")
            self.conn.rollback()
            return False


    def get_active_watchlist(self):
        """
        Fetches only active companies from the watchlist.
        Returns a list of symbols that have active=TRUE.
        """
        try:
            self.cursor.execute("SELECT symbol FROM watchlist WHERE active = TRUE")
            return [row["symbol"] for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error fetching active watchlist: {e}")
            return []

    def toggle_watchlist_status(self, symbol):
        """
        Toggle the active status of a symbol in the watchlist.

        Returns:
            True if toggled successfully, False otherwise.
        """
        try:
            # Check if the symbol exists
            self.cursor.execute("SELECT active FROM watchlist WHERE symbol = %s", (symbol,))
            row = self.cursor.fetchone()
            if not row:
                logger.warning(f"Symbol {symbol} not found in watchlist.")
                return False

            # Toggle the active status
            new_status = not row["active"]
            self.cursor.execute(
                "UPDATE watchlist SET active = %s WHERE symbol = %s",
                (new_status, symbol)
            )
            self.conn.commit()
            logger.info(f"Toggled active status for {symbol} to {new_status}.")
            return True

        except Exception as e:
            logger.error(f"Error toggling active status for {symbol}: {e}")
            self.conn.rollback()
            return False


    def close(self):
        self.cursor.close()
        self.conn.close()
        logger.info("DBManager connection closed")




