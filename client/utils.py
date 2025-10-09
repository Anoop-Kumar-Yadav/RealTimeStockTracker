from pathlib import Path
import pandas as pd
import yfinance as yf
import requests

API_BASE = "http://127.0.0.1:8000"

# ----------------- API HELPERS -----------------
def fetch_all_watchlist():
    try:
        resp = requests.get(f"{API_BASE}/watchlist/all")
        print(resp)
        resp.raise_for_status()
        return resp.json()["watchlist"]
    except:
        return []

def add_to_watchlist_api(symbol):
    try:
        resp = requests.post(f"{API_BASE}/watchlist/add", json={"symbol": symbol})
        return resp.status_code == 200
    except:
        return False

def remove_from_watchlist_api(symbol):
    try:
        resp = requests.post(f"{API_BASE}/watchlist/remove", json={"symbol": symbol})
        return resp.status_code == 200
    except:
        return False

def toggle_watchlist_status_api(symbol):
    try:
        resp = requests.post(f"{API_BASE}/watchlist/toggle", json={"symbol": symbol})
        return resp.status_code == 200
    except:
        return False

# ----------------- LOCAL CSV COMPANIES -----------------
from pathlib import Path
import pandas as pd
import yfinance as yf

def get_all_companies():
    try:
        base_path = Path(__file__).parent / "data"
        nasdaq_file = base_path / "nasdaqlisted.txt"
        other_file = base_path / "otherlisted.txt"

        all_companies = []

        for file in [nasdaq_file, other_file]:
            if not file.exists():
                raise FileNotFoundError(f"{file} does not exist")
            
            df = pd.read_csv(file, sep="|", encoding="utf-8", dtype=str)
            df.fillna("", inplace=True)
            for _, row in df.iterrows():
                symbol = row.get("Symbol", "").strip()
                name = row.get("Security Name", "").strip()
                if symbol and name:
                    all_companies.append((symbol, name))

        # Sort alphabetically by company name
        all_companies.sort(key=lambda x: x[1].lower())
        return all_companies

    except Exception as e:
        print(f"Error loading companies: {e}")
        return []


# ----------------- FETCH COMPANY INFO -----------------
def fetch_company_info(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        details = (
            f"Name: {info.get('shortName','N/A')}\n"
            f"Symbol: {symbol}\n"
            f"Sector: {info.get('sector','N/A')}\n"
            f"Industry: {info.get('industry','N/A')}\n"
            f"Market Cap: {info.get('marketCap','N/A')}\n"
            f"Previous Close: {info.get('previousClose','N/A')}\n"
            f"Open: {info.get('open','N/A')}\n"
            f"Day High / Low: {info.get('dayHigh','N/A')} / {info.get('dayLow','N/A')}\n"
            f"52 Week High / Low: {info.get('fiftyTwoWeekHigh','N/A')} / {info.get('fiftyTwoWeekLow','N/A')}\n"
            f"Website: {info.get('website','N/A')}\n"
            f"Description: {info.get('longBusinessSummary','N/A')[:500]}..."
        )
        return details
    except:
        return f"No details found for {symbol}"
