"""
Explore commodities data
"""

import requests
import pandas as pd
import os
from dotenv import load_dotenv
from pathlib import Path

API_FUNCTION = ["WTI", "BRENT", "NATURAL_GAS", "COPPER", "ALUMINUM",
                "WHEAT", "CORN", "COTTON", "SUGAR", "COFFEE", 
                "ALL_COMMODITIES"][1]

INTERVAL = ["daily", "weekly", "monthly"][0]

DATATYPE = ["json", "csv"][1]  # "json" or "csv"

outfolder = Path(__file__).parent / "examples"
# Load ALPHAVANTAGE_API_KEY from .env file
load_dotenv()
API_KEY = os.getenv('ALPHAVANTAGE_API_KEY')

TICKER = "NVDA"  # Example ticker symbol

url = f'https://www.alphavantage.co/query?function={API_FUNCTION}&interval={INTERVAL}&datatype={DATATYPE}&apikey={API_KEY}'
data = pd.read_csv(url) 


# Parse the main structure
print(data)