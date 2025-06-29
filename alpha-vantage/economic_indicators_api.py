"""
Explore commodities data
"""

import requests
import pandas as pd
import os
from dotenv import load_dotenv
from pathlib import Path

API_FUNCTION = ["REAL_GDP", "REAL_GDP_PER_CAPITA"][1]

INTERVAL = ["yearly", "quarterly"][1]

DATATYPE = ["json", "csv"][1]  # "json" or "csv"

outfolder = Path(__file__).parent / "examples"
# Load ALPHAVANTAGE_API_KEY from .env file
load_dotenv()
API_KEY = os.getenv('ALPHAVANTAGE_API_KEY')

url = f'https://www.alphavantage.co/query?function={API_FUNCTION}&interval={INTERVAL}&datatype={DATATYPE}&apikey={API_KEY}'
data = pd.read_csv(url) 


# Parse the main structure
print(data)