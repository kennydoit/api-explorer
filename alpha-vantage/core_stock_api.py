"""
Explor various functions of the Alpha Vantage API.
"""

import requests
import pandas as pd
import os
from dotenv import load_dotenv
from pathlib import Path

API_FUNCTION = "CORE_STOCK_API"

STOCK_API_FUNCTION = [
    "TIME_SERIES_INTRADAY", # 0
    "TIME_SERIES_DAILY", # 1
    "TIME_SERIES_WEEKLY", # 2
    "TIME_SERIES_MONTHLY", # 3
    "TIME_SERIES_DAILY_ADJUSTED", # 4
    "TIME_SERIES_WEEKLY_ADJUSTED", # 5  
    "TIME_SERIES_MONTHLY_ADJUSTED", # 6     
    "GLOBAL_QUOTE", # 7
    "SYMBOL_SEARCH", # 8
    "LISTING_STATUS" # 9
]

SYMBOL = "NVDA"
OUTPUT_SIZE = ["compact", "full"][0]  # "compact" or "full"
DATA_TYPE = ["json", "csv"][1]  # "json" or "csv"

outfolder = Path(__file__).parent / "examples"



# Load ALPHAVANTAGE_API_KEY from .env file
load_dotenv()

api_key = os.getenv('ALPHAVANTAGE_API_KEY')

for STOCK_API_FUNCTION in STOCK_API_FUNCTION:
    url = f'https://www.alphavantage.co/query?function={STOCK_API_FUNCTION}&symbol={SYMBOL}&outputsize={OUTPUT_SIZE}&datatype={DATA_TYPE}&apikey={api_key}'
    response = requests.get(url)
    df = pd.read_csv(url) if DATA_TYPE == "csv" else None
    output_file = outfolder / API_FUNCTION / f"{STOCK_API_FUNCTION}_{SYMBOL}_{OUTPUT_SIZE}.{DATA_TYPE}"
    df.to_csv(output_file, index=False) if DATA_TYPE == "csv" else None
    print("DataFrame Head:", df.head(100))

