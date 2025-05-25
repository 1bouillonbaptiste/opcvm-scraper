"""Define the fetch module.

This module uses Yahoo Finance to fetch data.
"""

from datetime import datetime
from typing import Any

import requests
import pandas as pd


def get_symbol_from_isin(isin: str) -> str:
    """Fetch the symbol from the ISIN."""
    search_url = "https://query2.finance.yahoo.com/v1/finance/search"
    search_params: dict[str, Any] = {
        "q": isin,
        "quotesCount": 1,
        "newsCount": 0,
        "enableFuzzyQuery": False,
        "quotesQueryId": "tss_match_phrase_query",
    }

    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(search_url, params=search_params, headers=headers)  # pyright: ignore
        response.raise_for_status()
        response_data: dict[str, Any] = response.json()
    except requests.RequestException as e:
        raise Exception(f"Error fetching symbol from ISIN: {e}")

    if not response_data.get("quotes"):
        raise ValueError(f"No symbol found for ISIN: {isin}")

    symbol = response_data["quotes"][0]["symbol"]

    return symbol


def fetch_historical_data(
    symbol: str, start_date: datetime, end_date: datetime
) -> pd.DataFrame:
    """Fetch historical data from Yahoo Finance."""
    hist_url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    params: dict[str, Any] = {
        "period1": start_date.date().strftime("%s"),
        "period2": end_date.date().strftime("%s"),
        "interval": "1d",
        "events": "history",
    }
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(hist_url, params=params, headers=headers)
        response.raise_for_status()
        response_data: dict[str, Any] = response.json()
    except requests.RequestException as e:
        raise Exception(f"Error fetching historical data: {e}")

    raw_data = response_data.get("chart", {}).get("result", [])

    if not raw_data:
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        raise ValueError(
            f"No historical data found for `{symbol}` between {start_date_str} and {end_date_str}."
        )

    timestamps = pd.to_datetime(pd.Series(raw_data[0]["timestamp"]), unit="s")
    quote_data = raw_data[0]["indicators"]["quote"][0]

    dataframe = pd.DataFrame(
        {
            "Date": timestamps,
            "Open": quote_data.get("open", []),
            "High": quote_data.get("high", []),
            "Low": quote_data.get("low", []),
            "Close": quote_data.get("close", []),
            "Volume": quote_data.get("volume", []),
        }
    )

    return dataframe
