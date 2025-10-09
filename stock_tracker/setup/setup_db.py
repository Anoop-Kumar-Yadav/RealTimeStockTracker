import pymysql
from pymysql.constants import CLIENT
from tracker import config
from logger_config import logger

def createDB():
    try:
        conn = pymysql.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            user=config.DB_USER,
            passwd=config.DB_PASSWORD,
            client_flag=CLIENT.MULTI_STATEMENTS
        )
        cursor = conn.cursor()

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config.DB_NAME};")
        logger.info(f"Database '{config.DB_NAME}' ensured!")

        cursor.execute(f"USE {config.DB_NAME};")

        create_table_query = """
        CREATE TABLE IF NOT EXISTS stocks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            symbol VARCHAR(10) NOT NULL,
            date DATE NOT NULL,
            open_price FLOAT,
            high_price FLOAT,
            low_price FLOAT,
            close_price FLOAT,
            volume BIGINT,
            sma FLOAT,
            rsi FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY unique_symbol_date (symbol, date),
            INDEX idx_symbol (symbol),
            INDEX idx_date (date)
        );
        """

        cursor.execute(create_table_query)
        logger.info("Table 'stocks' ensured!")

        create_watchlist_table = """
        CREATE TABLE IF NOT EXISTS watchlist (
            id INT AUTO_INCREMENT PRIMARY KEY,
            symbol VARCHAR(10) UNIQUE NOT NULL,
            active BOOLEAN DEFAULT TRUE,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_watchlist_table)
        logger.info("Table 'watchlist' ensured!")
        
        conn.commit()

    except Exception as e:
        logger.error(f"Error setting up database: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        logger.info("Database setup process finished.")


if __name__ == "__main__":
    createDB()
