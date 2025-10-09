from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST","localhost")
DB_PORT =  int(os.getenv("DB_PORT",3306))
DB_USER = os.getenv("DB_USER","root")
DB_PASSWORD = os.getenv("DB_PASSWORD","admin")
DB_NAME = os.getenv("DB_NAME","stock_tracker")

USE_YFINANACE = os.getenv("USE_YFINANCE","true").lower() in ("true",1,"yes")
ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY","GQ5DS63MNI7EZ9UD")

SMA_WINDOW = int(os.getenv("SMA_WINDOW",20))
RSI_PERIOD = int(os.getenv("RSI_PERIOD",14))

LOG_FILE = os.getenv("LOG_FILE","logs/app.log")