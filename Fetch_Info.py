import requests
import pandas as pd
from bs4 import BeautifulSoup
import os
import numpy as np
import yfinance as yf


def fetch_info():
    try:
        url = f"https://en.wikipedia.org/wiki/List_of_Dow_Jones_Industrial_Average_companies"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36,accept-language=en-US,en;q=0.9,accept:application/json"
        }
        # send get request to the Wikipedia page
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        # get symbols of Dow Jones components
        tables = soup.find_all("table")
        # convert table to DataFrame
        df = pd.read_html(str(tables))[0]
        # clean up
        df.drop(columns=['Notes'], inplace=True)
        return df

    except Exception as e:
        print(
            f"Error fetching info for Dow Jones Industrial Average from WIKI: {e}")
        return None


# get Dow Jones Industrial Average components
djia_components = fetch_info()
print(djia_components)
tickers = djia_components['Symbol'].tolist()
print(tickers)

# fetch historical data for the tickers
start_date = "2025-01-01"
end_date = "2025-12-31"
historical_data = yf.download(
    tickers, start=start_date, end=end_date, multi_level_index=False)
historical_data = historical_data['Close']
print(historical_data)

# calculate monthly returns
monthly_returns = historical_data.resample('M').ffill().pct_change()
print(monthly_returns)
