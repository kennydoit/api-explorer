"""
Explore technical indicators data
"""

import requests
import pandas as pd
import os
from dotenv import load_dotenv
from pathlib import Path

API_FUNCTION = ["ADX"][0]

SYMBOL = "NVDA"

INTERVAL = ["daily", "weekly", "monthly"][0]

DATATYPE = ["json", "csv"][1]  # "json" or "csv"

TIME_PERIOD = 30

outfolder = Path(__file__).parent / "examples"
# Load ALPHAVANTAGE_API_KEY from .env file
load_dotenv()
API_KEY = os.getenv('ALPHAVANTAGE_API_KEY')

url = f'https://www.alphavantage.co/query?function={API_FUNCTION}&symbol={SYMBOL}interval={INTERVAL}&datatype={DATATYPE}&time_period={TIME_PERIOD}&outputsize=compact&apikey={API_KEY}'
data = pd.read_csv(url) 


# Parse the main structure
print(data)


import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=WILLR&symbol=IBM&interval=daily&time_period=10&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)