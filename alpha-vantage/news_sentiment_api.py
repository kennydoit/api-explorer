"""
Explor various functions of the Alpha Vantage API.
"""

import requests
import pandas as pd
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

API_FUNCTION = "NEWS_SENTIMENT"

outfolder = Path(__file__).parent / "examples"
# Load ALPHAVANTAGE_API_KEY from .env file
load_dotenv()
API_KEY = os.getenv('ALPHAVANTAGE_API_KEY')

# Test historical data availability - try different time ranges
# Option 1: Maximum data (no time filter)
# url = f'https://www.alphavantage.co/query?function={API_FUNCTION}&tickers=NVDA&limit=1000&apikey={API_KEY}'

# Option 2: Try going back 1 year with sort=EARLIEST
# url = f'https://www.alphavantage.co/query?function={API_FUNCTION}&tickers=NVDA&time_from=20240101T0000&limit=1000&sort=EARLIEST&apikey={API_KEY}'

# Option 3: Try going back 2 years
# url = f'https://www.alphavantage.co/query?function={API_FUNCTION}&tickers=NVDA&time_from=20230101T0000&limit=1000&apikey={API_KEY}'

# Option 4: Try going back 5 years
#url = f'https://www.alphavantage.co/query?function={API_FUNCTION}&tickers=MSFT&time_from=20200101T0000&time_to=20201231T2359&limit=50&sort=EARLIEST&apikey={API_KEY}'
url = f'https://www.alphavantage.co/query?function={API_FUNCTION}&time_from=20200101T0000&limit=1000&sort=EARLIEST&apikey={API_KEY}'

# Option 5: Try going back 10 years
# url = f'https://www.alphavantage.co/query?function={API_FUNCTION}&tickers=NVDA&time_from=20150101T0000&limit=1000&sort=EARLIEST&apikey={API_KEY}'

response = requests.get(url)
data = response.json()

# Parse the main structure
print(f"📊 Total items: {data['items']}")
print(f"📰 Articles found: {len(data['feed'])}")

# Analyze date range and distribution
if len(data['feed']) > 0:
    dates = []
    for article in data['feed']:
        date_str = article['time_published'][:8]  # Extract YYYYMMDD
        dates.append(datetime.strptime(date_str, '%Y%m%d'))
    
    dates.sort()
    print(f"\n📅 HISTORICAL DATA ANALYSIS:")
    print("="*50)
    print(f"🗓️  Earliest article: {dates[0].strftime('%Y-%m-%d')}")
    print(f"🗓️  Latest article: {dates[-1].strftime('%Y-%m-%d')}")
    print(f"📊 Date range span: {(dates[-1] - dates[0]).days} days")
    
    # Count articles by year
    year_counts = {}
    for date in dates:
        year = date.year
        year_counts[year] = year_counts.get(year, 0) + 1
    
    print(f"\n📈 Articles by Year:")
    for year in sorted(year_counts.keys()):
        print(f"  {year}: {year_counts[year]} articles")
    
    # Count articles by month (last 12 months)
    from collections import Counter
    recent_dates = [d for d in dates if d >= datetime.now() - pd.DateOffset(months=12)]
    if recent_dates:
        month_counts = Counter([d.strftime('%Y-%m') for d in recent_dates])
        print(f"\n📈 Recent Monthly Distribution (last 12 months):")
        for month in sorted(month_counts.keys())[-12:]:
            print(f"  {month}: {month_counts[month]} articles")

print("\n" + "="*60)



# Parse individual articles
for i, article in enumerate(data['feed'][:3]):  # Show first 3 articles
    print(f"\n📰 Article {i+1}:")
    print(f"Title: {article['title']}")
    print(f"Source: {article['source']}")
    print(f"Published: {article['time_published']}")
    print(f"Overall Sentiment: {article['overall_sentiment_label']} ({article['overall_sentiment_score']:.3f})")
    
    # Show ticker-specific sentiment for NVDA
    print(f"\n📈 Ticker Sentiments:")
    for ticker_info in article['ticker_sentiment']:
        if ticker_info['ticker'] == 'MSFT':
            print(f"  {ticker_info['ticker']}: {ticker_info['ticker_sentiment_label']} "
                  f"(Score: {ticker_info['ticker_sentiment_score']}, "
                  f"Relevance: {ticker_info['relevance_score']})")
    
    print(f"\n📝 Summary: {article['summary'][:200]}...")
    print("-" * 60)

# Create summary statistics
print(f"\n🎯 SUMMARY STATISTICS:")
print("="*40)

# Count sentiment labels
sentiment_counts = {}
for article in data['feed']:
    sentiment = article['overall_sentiment_label']
    sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1

print(f"📊 Overall Sentiment Distribution:")
for sentiment, count in sentiment_counts.items():
    percentage = (count / len(data['feed'])) * 100
    print(f"  {sentiment}: {count} articles ({percentage:.1f}%)")

# Analyze your specific tickers
target_tickers = ['MSFT']  # Focus only on NVDA
ticker_sentiment_data = {ticker: [] for ticker in target_tickers}

for article in data['feed']:
    for ticker_info in article['ticker_sentiment']:
        if ticker_info['ticker'] in target_tickers:
            ticker_sentiment_data[ticker_info['ticker']].append({
                'score': float(ticker_info['ticker_sentiment_score']),
                'label': ticker_info['ticker_sentiment_label'],
                'relevance': float(ticker_info['relevance_score'])
            })

print(f"\n📈 Ticker Analysis:")
for ticker in target_tickers:
    if ticker_sentiment_data[ticker]:
        scores = [item['score'] for item in ticker_sentiment_data[ticker]]
        avg_score = sum(scores) / len(scores)
        mentions = len(ticker_sentiment_data[ticker])
        print(f"  {ticker}: {mentions} mentions, Avg sentiment: {avg_score:.3f}")

# Uncomment the next line to stop execution here (skip time series creation)
# exit()

# Create daily time series data for stock analysis
from datetime import datetime
import json

print(f"\n📅 CREATING DAILY TIME SERIES:")
print("="*40)

# Aggregate sentiment data by date and ticker
daily_data = {}

for article in data['feed']:
    # Parse the date from time_published (format: YYYYMMDDTHHMMSS)
    date_str = article['time_published'][:8]  # Extract YYYYMMDD
    date = datetime.strptime(date_str, '%Y%m%d').strftime('%Y-%m-%d')
    
    for ticker_info in article['ticker_sentiment']:
        if ticker_info['ticker'] in target_tickers:
            ticker = ticker_info['ticker']
            key = (date, ticker)
            
            if key not in daily_data:
                daily_data[key] = {
                    'date': date,
                    'ticker': ticker,
                    'articles': [],
                    'sentiment_scores': [],
                    'relevance_scores': [],
                    'sentiment_labels': []
                }
            
            daily_data[key]['articles'].append(article['title'])
            daily_data[key]['sentiment_scores'].append(float(ticker_info['ticker_sentiment_score']))
            daily_data[key]['relevance_scores'].append(float(ticker_info['relevance_score']))
            daily_data[key]['sentiment_labels'].append(ticker_info['ticker_sentiment_label'])

# Convert to DataFrame for time series analysis
time_series_data = []

for (date, ticker), day_data in daily_data.items():
    scores = day_data['sentiment_scores']
    relevances = day_data['relevance_scores']
    
    # Calculate various aggregations
    avg_sentiment = sum(scores) / len(scores)
    
    # Weighted average by relevance
    weighted_sentiment = sum(s * r for s, r in zip(scores, relevances)) / sum(relevances) if sum(relevances) > 0 else avg_sentiment
    
    # Count sentiment labels
    positive_count = day_data['sentiment_labels'].count('Bullish')
    negative_count = day_data['sentiment_labels'].count('Bearish')
    neutral_count = day_data['sentiment_labels'].count('Neutral')
    
    time_series_data.append({
        'date': date,
        'ticker': ticker,
        'article_count': len(scores),
        'avg_sentiment_score': round(avg_sentiment, 4),
        'weighted_sentiment_score': round(weighted_sentiment, 4),
        'avg_relevance_score': round(sum(relevances) / len(relevances), 4),
        'bullish_mentions': positive_count,
        'bearish_mentions': negative_count,
        'neutral_mentions': neutral_count,
        'sentiment_ratio': round((positive_count - negative_count) / len(scores), 4) if len(scores) > 0 else 0
    })

# Create DataFrame and sort by date and ticker
df_timeseries = pd.DataFrame(time_series_data)

if not df_timeseries.empty and 'date' in df_timeseries.columns:
    df_timeseries['date'] = pd.to_datetime(df_timeseries['date'])
    df_timeseries = df_timeseries.sort_values(['date', 'ticker']).reset_index(drop=True)
else:
    print("⚠️ No time series data created - DataFrame is empty or missing 'date' column")
    exit()

print(f"📊 Time series created with {len(df_timeseries)} daily observations")
print(f"📅 Date range: {df_timeseries['date'].min().strftime('%Y-%m-%d')} to {df_timeseries['date'].max().strftime('%Y-%m-%d')}")
print(f"📈 Tickers: {', '.join(df_timeseries['ticker'].unique())}")

# Display sample of the time series
print(f"\n🔍 Sample of Daily Time Series:")
print(df_timeseries.head(10).to_string(index=False))

# Show summary statistics
print(f"\n📊 Summary Statistics by Ticker:")
summary = df_timeseries.groupby('ticker').agg({
    'avg_sentiment_score': ['mean', 'std'],
    'article_count': 'sum',
    'sentiment_ratio': 'mean'
}).round(4)
print(summary)

# Save both raw data and time series
output_file = outfolder / "news_sentiment_data.json"
timeseries_file = outfolder / "daily_sentiment_timeseries.csv"

output_file.parent.mkdir(parents=True, exist_ok=True)

# Save raw data
with open(output_file, 'w') as f:
    json.dump(data, f, indent=2)

# Save time series
df_timeseries.to_csv(timeseries_file, index=False)

print(f"\n💾 Raw data saved to: {output_file}")
print(f"💾 Daily time series saved to: {timeseries_file}")

print(f"\n✅ Ready for stock market analysis!")
print(f"📈 You can now merge this with stock price data on 'date' and 'ticker' columns")
print(f"🔍 Key columns for analysis:")
print(f"  - avg_sentiment_score: Simple average of all sentiment scores for the day")
print(f"  - weighted_sentiment_score: Relevance-weighted sentiment score")
print(f"  - sentiment_ratio: (bullish - bearish) / total mentions")
print(f"  - article_count: Number of news mentions per day")

# Create Daily Time Series Data
print(f"\n📈 CREATING DAILY TIME SERIES:")
print("="*50)

from datetime import datetime
from collections import defaultdict

# Convert to daily time series
daily_sentiment = defaultdict(lambda: defaultdict(list))

for article in data['feed']:
    # Parse the date from time_published (format: 20250628T101500)
    date_str = article['time_published'][:8]  # Get YYYYMMDD
    date = datetime.strptime(date_str, '%Y%m%d').strftime('%Y-%m-%d')
    
    # Add overall article sentiment
    daily_sentiment[date]['overall'].append(float(article['overall_sentiment_score']))
    
    # Add ticker-specific sentiment
    for ticker_info in article['ticker_sentiment']:
        if ticker_info['ticker'] in target_tickers:
            daily_sentiment[date][ticker_info['ticker']].append({
                'sentiment_score': float(ticker_info['ticker_sentiment_score']),
                'relevance_score': float(ticker_info['relevance_score'])
            })

# Aggregate daily sentiment data
daily_aggregated = []

for date in sorted(daily_sentiment.keys()):
    row = {'date': date}
    
    # Overall market sentiment for the day
    if daily_sentiment[date]['overall']:
        row['overall_sentiment_avg'] = sum(daily_sentiment[date]['overall']) / len(daily_sentiment[date]['overall'])
        row['article_count'] = len(daily_sentiment[date]['overall'])
    
    # Ticker-specific sentiment
    for ticker in target_tickers:
        if daily_sentiment[date][ticker]:
            # Simple average
            sentiment_scores = [item['sentiment_score'] for item in daily_sentiment[date][ticker]]
            relevance_scores = [item['relevance_score'] for item in daily_sentiment[date][ticker]]
            
            row[f'{ticker}_sentiment_avg'] = sum(sentiment_scores) / len(sentiment_scores)
            row[f'{ticker}_relevance_avg'] = sum(relevance_scores) / len(relevance_scores)
            row[f'{ticker}_mention_count'] = len(sentiment_scores)
            
            # Weighted average (sentiment weighted by relevance)
            if relevance_scores:
                weighted_sentiment = sum(s * r for s, r in zip(sentiment_scores, relevance_scores))
                total_relevance = sum(relevance_scores)
                row[f'{ticker}_sentiment_weighted'] = weighted_sentiment / total_relevance if total_relevance > 0 else 0
        else:
            # Fill missing data with neutral values
            row[f'{ticker}_sentiment_avg'] = 0.0
            row[f'{ticker}_relevance_avg'] = 0.0
            row[f'{ticker}_mention_count'] = 0
            row[f'{ticker}_sentiment_weighted'] = 0.0
    
    daily_aggregated.append(row)

# Create DataFrame for easy analysis
df = pd.DataFrame(daily_aggregated)
print(f"📊 Daily time series created: {len(df)} days")
print(f"📅 Date range: {df['date'].min()} to {df['date'].max()}")
print("\nFirst few rows:")
print(df.head())

# Save to CSV for use in other analysis
csv_file = outfolder / "daily_sentiment_timeseries.csv"
df.to_csv(csv_file, index=False)
print(f"\n💾 Daily time series saved to: {csv_file}")

# Create a summary statistics table
print(f"\n📈 DAILY SENTIMENT SUMMARY:")
print("-" * 50)
for ticker in target_tickers:
    sentiment_col = f'{ticker}_sentiment_weighted'
    if sentiment_col in df.columns:
        avg_sentiment = df[sentiment_col].mean()
        std_sentiment = df[sentiment_col].std()
        total_mentions = df[f'{ticker}_mention_count'].sum()
        print(f"{ticker}: Avg={avg_sentiment:.3f}, Std={std_sentiment:.3f}, Total mentions={total_mentions}")

# Create visualization-ready data
print(f"\n📊 SAMPLE ANALYSIS - Recent Trend:")
print("-" * 40)
# Show last 5 days trend
recent_df = df.tail(5)
for _, row in recent_df.iterrows():
    print(f"{row['date']}: ", end="")
    for ticker in target_tickers:
        sentiment = row[f'{ticker}_sentiment_weighted']
        mentions = row[f'{ticker}_mention_count']
        print(f"{ticker}:{sentiment:.2f}({mentions}) ", end="")
    print()

print(f"\n🎯 TIP: Use the CSV file for:")
print("  - Merging with stock price data")
print("  - Creating correlation analysis")
print("  - Building predictive models")
print("  - Plotting sentiment vs. price trends")
