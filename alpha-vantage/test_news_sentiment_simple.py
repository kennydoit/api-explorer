"""
Simple test script for Alpha Vantage NEWS_SENTIMENT API
Based directly on the official documentation examples
"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('ALPHAVANTAGE_API_KEY')

print(f"🔑 Using API key: {api_key[:10]}...{api_key[-4:] if api_key else 'None'}")
print("="*60)

# Test 1: Try the EXACT example from Alpha Vantage documentation
print("🧪 TEST 1: Alpha Vantage Documentation Example")
print("URL from docs: https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=AAPL&apikey=demo")

doc_url = "https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=AAPL&apikey=demo"
try:
    response = requests.get(doc_url)
    print(f"📡 Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        items = data.get('items', '0')
        print(f"📊 Items in response: {items}")
        print(f"🔑 Response keys: {list(data.keys())}")
        
        if 'feed' in data and data['feed']:
            print(f"✅ SUCCESS! Documentation example works - {len(data['feed'])} articles found")
            print(f"📰 Sample headline: {data['feed'][0].get('title', 'No title')[:80]}...")
        else:
            print("⚠️ No feed data in documentation example")
    else:
        print(f"❌ Documentation example failed with status {response.status_code}")
        
except Exception as e:
    print(f"❌ Error with documentation example: {e}")

print("\n" + "="*60)

# Test 2: Use YOUR API key with the exact same simple query
print("🧪 TEST 2: Your API Key with Simple AAPL Query")
your_url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=AAPL&apikey={api_key}"
print(f"Your URL: {your_url}")

try:
    response = requests.get(your_url)
    print(f"📡 Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        items = data.get('items', '0')
        print(f"📊 Items in response: {items}")
        print(f"🔑 Response keys: {list(data.keys())}")
        
        # Check for API limit messages
        if 'Information' in data:
            print(f"ℹ️ API Information: {data['Information']}")
        if 'Note' in data:
            print(f"📝 API Note: {data['Note']}")
            
        if 'feed' in data and data['feed']:
            print(f"✅ SUCCESS! Your API works - {len(data['feed'])} articles found")
            print(f"📰 Sample headline: {data['feed'][0].get('title', 'No title')[:80]}...")
            
            # Save successful result
            with open('successful_news_response.json', 'w') as f:
                json.dump(data, f, indent=2)
            print(f"💾 Response saved to successful_news_response.json")
        else:
            print("⚠️ No feed data with your API key")
            # Show full response for debugging
            print(f"📄 Full response: {json.dumps(data, indent=2)}")
    else:
        print(f"❌ Your API failed with status {response.status_code}")
        print(f"📄 Response: {response.text}")
        
except Exception as e:
    print(f"❌ Error with your API: {e}")

print("\n" + "="*60)

# Test 3: Try without any parameters except the function
print("🧪 TEST 3: Minimal Query (No Parameters)")
minimal_url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&apikey={api_key}"
print(f"Minimal URL: {minimal_url}")

try:
    response = requests.get(minimal_url)
    print(f"📡 Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        items = data.get('items', '0')
        print(f"📊 Items in response: {items}")
        
        if 'feed' in data and data['feed']:
            print(f"✅ Minimal query works - {len(data['feed'])} articles found")
        else:
            print("⚠️ Minimal query returned no feed data")
            
except Exception as e:
    print(f"❌ Error with minimal query: {e}")

print("\n" + "="*60)

# Test 4: Try different stocks
print("🧪 TEST 4: Different Stocks")
test_stocks = ["NVDA", "MSFT", "TSLA", "META"]

for stock in test_stocks:
    stock_url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={stock}&apikey={api_key}"
    print(f"\n📈 Testing {stock}...")
    
    try:
        response = requests.get(stock_url)
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', '0')
            if 'feed' in data and data['feed']:
                print(f"  ✅ {stock}: {len(data['feed'])} articles")
            else:
                print(f"  ❌ {stock}: No articles")
        else:
            print(f"  ❌ {stock}: HTTP {response.status_code}")
    except Exception as e:
        print(f"  ❌ {stock}: Error - {e}")

print("\n" + "="*60)
print("🎯 CONCLUSION:")
print("If Test 1 (documentation example) works but Test 2 (your API) doesn't,")
print("then there might be an issue with your API key or account limitations.")
print("If none of the tests work, there might be a broader API issue.")
