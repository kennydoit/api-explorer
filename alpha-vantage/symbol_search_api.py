

import requests
import pandas as pd
import os
from dotenv import load_dotenv
from pathlib import Path

API_FUNCTION = "CORE_STOCK_API"
STOCK_API_FUNCTION = "SYMBOL_SEARCH"
KEYWORDS = "NVDA"

outfolder = Path(__file__).parent / "examples"



# Load ALPHAVANTAGE_API_KEY from .env file
load_dotenv()

api_key = os.getenv('ALPHAVANTAGE_API_KEY')

url = f'https://www.alphavantage.co/query?function={STOCK_API_FUNCTION}&keywords={KEYWORDS}&datatype=csv&apikey={api_key}'
response = requests.get(url)
df = pd.read_csv(url) 
output_file = outfolder / API_FUNCTION / f"{STOCK_API_FUNCTION}_{KEYWORDS}.csv"
df.to_csv(output_file, index=False) 
print("DataFrame Head:", df.head(100))


