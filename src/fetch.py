"""Define the fetch module.

This module uses Yahoo Finance to fetch data.
"""

from typing import Any

import requests


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
