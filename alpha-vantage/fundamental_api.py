"""
Explore fundamental data
"""

import requests
import pandas as pd
import os
from dotenv import load_dotenv
from pathlib import Path

API_FUNCTION = ["OVERVIEW", "DIVIDENDS", "SPLITS", "INCOME_STATEMENT", "BALANCE_SHEET",
                "CASH_FLOW", "EARNINGS", "LISTING_STATUS", "EARNINGS_CALENDAR",
                "IPO_CALENDAR"][7]

print("API_FUNCTION:", API_FUNCTION)

outfolder = Path(__file__).parent / "examples" / "FUNDAMENTAL_DATA"
# Load ALPHAVANTAGE_API_KEY from .env file
load_dotenv()
API_KEY = os.getenv('ALPHAVANTAGE_API_KEY')

TICKER = "NVDA"  # Example ticker symbol

if API_FUNCTION == "OVERVIEW":
    url = f'https://www.alphavantage.co/query?function={API_FUNCTION}&symbol={TICKER}&apikey={API_KEY}'
    print("Fetching data from:", url)
    response = requests.get(url)
    data = response.json()
    print("Response status:", response.status_code)
    print("Response content:", response.text)
    print("JSON data:", data)
    data = pd.DataFrame.from_dict(data, orient='index', columns=['Value'])
    print("DataFrame Head:", data.head(100))
    output_type = 'df'
elif API_FUNCTION == "EARNINGS_CALENDAR":
    url = f'https://www.alphavantage.co/query?function={API_FUNCTION}&apikey={API_KEY}'
    data = pd.read_csv(url) 
    output_type = 'df'
elif API_FUNCTION == "IPO_CALENDAR":
    url = f'https://www.alphavantage.co/query?function={API_FUNCTION}&horizon=12month&apikey={API_KEY}'
    data = pd.read_csv(url)
    output_type = 'df'
elif API_FUNCTION == "LISTING_STATUS":
    url = f'https://www.alphavantage.co/query?function={API_FUNCTION}&apikey={API_KEY}'
    response = requests.get(url)
    data = pd.read_csv(url) 
    output_type = 'df_noticker'    
else:
    url = f'https://www.alphavantage.co/query?function={API_FUNCTION}&symbol={TICKER}&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    output_type = 'json'

if output_type == 'df':
    output_file = outfolder / f"{API_FUNCTION}_{TICKER}.csv"
    data.to_csv(output_file, index=True)
    print("Output saved to:", output_file)
    print("DataFrame Head:", data.head(100))
elif output_type == 'df_noticker':
    output_file = outfolder / f"{API_FUNCTION}.csv"
    data.to_csv(output_file, index=True)
    print("Output saved to:", output_file)
    print("DataFrame Head:", data.head(100))


