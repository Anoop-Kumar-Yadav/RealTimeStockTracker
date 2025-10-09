# backend_api.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from db_manager import DBManager
import pandas as pd

app = FastAPI(title="Stock Watchlist API")

# Allow frontend CORS requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = DBManager()

import requests

def trigger_scheduler():
    try:
        resp = requests.post("http://localhost:8081/api/scheduler/trigger-python-job")
    except Exception as e:
        print("Failed to trigger scheduler:", e)

# Call this after your stock data is inserted/updated



# ----------------- Pydantic models -----------------
class SymbolRequest(BaseModel):
    symbol: str

# ----------------- Watchlist Endpoints -----------------
@app.get("/watchlist/active")
def get_active_watchlist():
    try:
        symbols = db.get_active_watchlist()
        return {"watchlist": symbols}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/watchlist/all")
def get_all_watchlist():
    try:
        items = db.fetch_watchlist()  # returns [(symbol, active), ...]
        return {"watchlist": [{"symbol": s, "active": a} for s, a in items]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/watchlist/add")
def add_to_watchlist(req: SymbolRequest):
    success = db.add_to_watchlist(req.symbol.upper())
    if success["status"]:
        trigger_scheduler()
        return {"message": f"{req.symbol.upper()} added in watchlist"}

    else:
        raise HTTPException(status_code=500, detail=f"Failed to add {req.symbol.upper()}")

@app.post("/watchlist/remove")
def remove_from_watchlist(req: SymbolRequest):
    success = db.remove_from_watchlist(req.symbol.upper())
    if success:
        trigger_scheduler()
        return {"message": f"{req.symbol.upper()} removed from watchlist"}
    else:
        raise HTTPException(status_code=500, detail=f"Failed to remove {req.symbol.upper()}")

@app.post("/watchlist/toggle")
def toggle_watchlist_status(req: SymbolRequest):
    success = db.toggle_watchlist_status(req.symbol.upper())
    if success:
        trigger_scheduler()
        return {"message": f"{req.symbol.upper()} active status toggled"}
    else:
        raise HTTPException(status_code=500, detail=f"Failed to toggle status for {req.symbol.upper()}")


