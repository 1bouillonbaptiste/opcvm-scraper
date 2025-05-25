"""Define the fetch module.

This module uses Yahoo Finance to fetch data.
"""

from datetime import datetime
from typing import Any

import requests
import pandas as pd


def send_request(url: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    """Send a GET request to the given url."""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, params=params, headers=headers)
    try:
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise Exception(f"Error requesting data: {e}")


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

    data = send_request(search_url, search_params)

    if not data.get("quotes"):
        raise ValueError(f"No symbol found for ISIN: {isin}")

    symbol = data["quotes"][0]["symbol"]

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
    data = send_request(hist_url, params)

    raw_data = data.get("chart", {}).get("result", [])

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
            "date": timestamps,
            "open": quote_data.get("open", []),
            "high": quote_data.get("high", []),
            "low": quote_data.get("low", []),
            "close": quote_data.get("close", []),
            "volume": quote_data.get("volume", []),
        }
    )

    return dataframe
