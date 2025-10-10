# 📈 Real-Time Stock Tracker & Watchlist Manager

> Track stocks, monitor trends, and never miss a market move with automated updates and beautiful visualizations.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-Desktop-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 🏗️ Architecture and Data Flow
   
   ![Architecture Diagram](https://github.com/Anoop-Kumar-Yadav/RealTimeStockTracker/raw/main/readme_resources/screenshots/architecture.svg)
   ![Architecture Diagram](https://github.com/Anoop-Kumar-Yadav/RealTimeStockTracker/raw/main/readme_resources/screenshots/RealTimeStockTracker.drawio.png)
### Component Details

**1. Client (Frontend) - PyQt5**
- Files: `client/app.py`, `client/utils.py`
- Features:
  - Company dropdown with autocomplete
  - Display stock information (price, SMA, RSI)
  - Add/remove/toggle watchlist items
  - Communicates with FastAPI backend

**2. API Layer (Backend) - FastAPI**
- File: `stock_tracker/tracker/backend_api.py`
- Key Endpoints:
  
  | Endpoint | Method | Description |
  |----------|--------|-------------|
  | `/watchlist/all` | GET | Get all watchlist items |
  | `/watchlist/active` | GET | Get only active watchlist |
  | `/watchlist/add` | POST | Add symbol to watchlist |
  | `/watchlist/remove` | DELETE | Remove symbol from watchlist |
  | `/watchlist/toggle` | PUT | Toggle active/inactive status |

**3. Scheduler Server - Java Quartz**
- Location: `stock_tracker/java_scheduler/stock-tracker-scheduler/`
- Technology: Spring Boot + Quartz
- Function:
  - Triggers Python script at specified intervals
  - Default: Market close time or every 10 seconds (for testing)
  - Executes `main.py` automatically

**4. Data Processing - Python Scripts**
- Files in `stock_tracker/tracker/`:
  - `main.py` - Main execution script
  - `api_fetcher.py` - Fetches stock data from yfinance/Alpha Vantage
  - `indicator_calculator.py` - Calculates SMA and RSI
  - `db_manager.py` - Database operations
  - `config.py` - Configuration settings
  - `logger_config.py` - Logging setup


**5. Visualization - Power BI**
- Connects directly to MySQL database
- Displays:
  - Real-time price charts
  - Historical trends
  - Technical indicators (SMA, RSI)
  - Watchlist overview
- Auto-refreshes after scheduler updates data

---

## 🔄 Complete Workflow

### Step-by-Step Process

**1. User Interaction**
```
User opens PyQt5 app
    ↓
Searches for company
    ↓
Views company info 
    ↓
Clicks "Add to Watchlist"
    ↓
PyQt5 sends POST request to FastAPI
```

**2. Backend Processing**
```
FastAPI receives request
    ↓
Validates symbol
    ↓
Inserts into watchlist table
    ↓
Returns success response
    ↓
PyQt5 updates UI
```

**3. Automated Data Fetching**
```
Java Scheduler triggers (market close / interval)
    ↓
Executes Python main.py script
    ↓
main.py calls api_fetcher.py
    ↓
Fetches data from yfinance
    ↓
indicator_calculator.py computes SMA & RSI
    ↓
db_manager.py inserts data into stocks table
    ↓
Logger records operation in logs/
```

**4. Visualization Update**
```
Power BI connects to MySQL
    ↓
Queries stocks table
    ↓
Updates charts with new data
    ↓
User sees live trends and indicators
```

---

## 🛠️ Tech Stack

| Component | Technology | Why? |
|-----------|-----------|------|
| Frontend | PyQt5 | Rich desktop UI with great widgets |
| API | FastAPI | Fast, Python API |
| Backend | Python 3.8+ | Easy data manipulation with pandas |
| Scheduler | Java Quartz | Task Scheduling |
| Database | MySQL | Relational database |
| Data Source | yfinance | Free, reliable stock data |
| Visualization | Power BI | dashboards |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Java 11 or higher
- MySQL 8.0 
- Power BI Desktop (optional)

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/Anoop-Kumar-Yadav/RealTimeStockTracker.git
cd RealTimeStockTracker
```
## ⚙️ Configuration

**Backend Configuration** (`stock_tracker\setup\.env.template`)
```python
# Database credentials
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password ( required )
DB_NAME=stock_tracker     ( required )

# API selection
USE_YFINANCE=true
ALPHA_VANTAGE_KEY="your vanatage api key" (optional)

# Indicators
SMA_WINDOW=20
RSI_PERIOD=14

# Logs
LOG_FILE=logs/app.log

```

**Scheduler Configuration** (`scheduler/application.properties`)
```properties
spring.application.name=stock-tracker-scheduler
server.port=8081 (required)
```

---

## 💻 Usage

### Basic Workflow

```bash
# Terminal 1: Start API
cd stock_tracker/tracker && uvicorn backend_api:app --reload

# Terminal 2: Start Frontend
cd client && python app.py

# Terminal 3: Start Scheduler 
cd stock_tracker/java_scheduler/stock-tracker-scheduler; mvn spring-boot:run 
```

### Using the App

1. **Search for a Stock**
   - Type symbol or Select (e.g., `AAPL`) or company name (e.g., `Apple`)
   - Click on "Show Info" Button or Press Enter

2. **View Stock Details**
   - Name: Apple Inc.
   - Symbol: AAPL
   - Sector: Technology
   - Industry: Consumer Electronics
   - Market Cap: 3770052509696
   - Previous Close: 258.06
   - Open: 257.9
   - Day High / Low: 258.0 / 253.1402
   - 52 Week High / Low: 260.1 / 169.21
   - Website: https://www.apple.com
   - Description: Apple Inc. designs, manufactures, and markets smartphones... 

3. **Manage Watchlist**
   - Click "Add to Watchlist" to track
   - Toggle active/inactive status
   - Remove unwanted stocks

4. **Automated Updates**
   - Scheduler runs daily at configured time
   - Fetches latest data for all watchlist stocks
   - Updates database automatically

---



## 📁 Project Structure

```
REALTIMESTOCKTRACKER/
│
├── 📂 .vscode/                      # VS Code configuration
│
├── 📂 client/                       # PyQt5 Desktop Application
│   ├── 📂 __pycache__/              # Python cache files
│   ├── 📂 data/                     # Data files
│   │   ├── 📄 nasdaqlisted.txt      # NASDAQ stock list
│   │   └── 📄 otherlisted.txt       # Other exchange stocks
│   ├── 🐍 app.py                    # Main application file
│   └── 🐍 utils.py                  # Utility functions
│
├── 📂 stock_tracker/                # Java Scheduler Project
│   ├── 📂 java_scheduler\           # Scheduler implementation
│   │   └── stock-tracker-scheduler/ # Spring Boot scheduler
│   │       ├── 📂 .mvn/             # Maven wrapper
│   │       ├── 📂 src/              # Java source files
│   │       ├── 📂 target/           # Compiled files
│   │       ├── 📄 HELP.md           # Maven help
│   │       ├── 📄 mvnw              # Maven wrapper (Unix)
│   │       ├── 📄 mvnw.cmd          # Maven wrapper (Windows)
│   │       └── 📄 pom.xml           # Maven configuration
│   ├── 📂 logs/                     # Application logs
│   ├── 📂 setup/                    # Setup scripts
│   │   ├── 📂 __pycache__/          # Python cache
│   │   ├── 📄 .env.template         # Environment template
│   │   ├── 📄 requirements.txt      # Python dependencies
│   │   └── 🐍 setup_db.py           # Database setup script
│   └── 📂 tracker/                  # Backend API & Scripts
│       ├── 📂 __pycache__/          # Python cache
│       ├── 🐍 __init__.py           # Package initializer
│       ├── 🐍 api_fetcher.py        # Stock data fetcher
│       ├── 🐍 backend_api.py        # FastAPI REST API
│       ├── 🐍 config.py             # Configuration settings
│       ├── 🐍 db_manager.py         # Database operations
│       ├── 🐍 indicator_calculator.py # SMA/RSI calculations
│       ├── 🐍 logger_config.py      # Logging configuration
│       └── 🐍 main.py               # Main scheduler script
│
├── 📂 venv/                         # Python virtual environment
│
├── 📄 .gitattributes                # Git attributes
│
└── 📄 README.md                     # You are here!
```

### Key Directories Explained

| Directory | Purpose |
|-----------|---------|
| `client/` | PyQt5 desktop application with UI and stock data lists |
| `stock_tracker/tracker/` | Core backend with FastAPI, data fetching, and calculations |
| `stock_tracker/java_scheduler/` | Java Quartz scheduler for automated updates |
| `stock_tracker/setup/` | Database setup scripts and environment configuration |
| `stock_tracker/logs/` | Application logs for debugging |
| `venv/` | Python virtual environment (not in git) |

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/watchlist/active` | Fetch all active symbols in the watchlist |
| `GET` | `/watchlist/all` | Fetch all watchlist entries with active status |
| `POST` | `/watchlist/add` | Add a symbol to the watchlist (reactivate if inactive) |
| `POST` | `/watchlist/remove` | Remove a symbol from the watchlist (set active=False) |
| `POST` | `/watchlist/toggle` | Toggle the active/inactive status of a watchlist symbol |

---

## 🎨 Screenshots

### Desktop Application
![Client UI Screenshot](https://github.com/Anoop-Kumar-Yadav/RealTimeStockTracker/raw/main/readme_resources/screenshots/client_ui.png)


### Power BI Dashboard
![Power BI](https://github.com/Anoop-Kumar-Yadav/RealTimeStockTracker/raw/main/readme_resources/screenshots/stocks_tracker_page-0001.jpg)
![Power BI](https://github.com/Anoop-Kumar-Yadav/RealTimeStockTracker/raw/main/readme_resources/screenshots/stocks_tracker_page-0002.jpg)
---

## 🚧 Roadmap

**Version 1.0** ✅
- [x] Basic stock search
- [x] Watchlist management
- [x] SMA & RSI indicators
- [x] Automated scheduling

**Version 2.0 (Future Scope)** 🔄
- [ ] User authentication
- [ ] Multiple portfolios
- [ ] Email alerts
- [ ] Mobile app

**Version 3.0 (Future Scope)** 📅
- [ ] Machine learning predictions

---


## 📝 License

This project is licensed under the MIT License.

```
MIT License - Copyright (c) 2025 Anoop Kumar Yadav
```

---

## 👤 Author

**Anoop Kumar Yadav**

- 🌐 GitHub: [@Anoop-Kumar-Yadav](https://github.com/Anoop-Kumar-Yadav)
- 💼 LinkedIn: [Anoop Kumar Yadav](https://www.linkedin.com/in/anoop-kumar-yadav-9b31b3283/)
- 📧 Email: anoop9569110314@example.com

---

## 🙏 Acknowledgments

Special thanks to:
- [yfinance](https://github.com/ranaroussi/yfinance) for stock data
- [FastAPI](https://fastapi.tiangolo.com/) for the amazing framework
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) for the GUI toolkit
- ChatGPT and Claude for guidance and assistance in designing and implementing this project

---

<div align="center">

**Built with ❤️ by Anoop Kumar Yadav**

[⬆ Back to Top](#-real-time-stock-tracker--watchlist-manager)

</div>
