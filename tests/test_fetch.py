from src.fetch import get_symbol_from_isin, fetch_historical_data

from datetime import datetime
from unittest.mock import patch
import pytest


@patch("src.fetch.send_request")
def test_get_symbol_from_isin(mock_send_request):
    mock_send_request.return_value = {"quotes": [{"symbol": "AAPL"}]}

    assert get_symbol_from_isin("US0378331005") == "AAPL"


@pytest.fixture
def historical_data():
    return {
        "chart": {
            "result": [
                {
                    "meta": {
                        "currency": "USD",
                        "symbol": "AAPL",
                        "exchangeName": "NMS",
                        "fullExchangeName": "NasdaqGS",
                        "instrumentType": "EQUITY",
                        "firstTradeDate": 345479400,
                        "regularMarketTime": 1748030401,
                        "hasPrePostMarketData": True,
                        "gmtoffset": -14400,
                        "timezone": "EDT",
                        "exchangeTimezoneName": "America/New_York",
                        "regularMarketPrice": 195.27,
                        "fiftyTwoWeekHigh": 260.1,
                        "fiftyTwoWeekLow": 169.21,
                        "regularMarketDayHigh": 197.7,
                        "regularMarketDayLow": 193.46,
                        "regularMarketVolume": 77631468,
                        "longName": "Apple Inc.",
                        "shortName": "Apple Inc.",
                        "chartPreviousClose": 129.93,
                        "priceHint": 2,
                        "currentTradingPeriod": {
                            "pre": {
                                "timezone": "EDT",
                                "end": 1748007000,
                                "start": 1747987200,
                                "gmtoffset": -14400,
                            },
                            "regular": {
                                "timezone": "EDT",
                                "end": 1748030400,
                                "start": 1748007000,
                                "gmtoffset": -14400,
                            },
                            "post": {
                                "timezone": "EDT",
                                "end": 1748044800,
                                "start": 1748030400,
                                "gmtoffset": -14400,
                            },
                        },
                        "dataGranularity": "1d",
                        "range": "",
                        "validRanges": [
                            "1d",
                            "5d",
                            "1mo",
                            "3mo",
                            "6mo",
                            "1y",
                            "2y",
                            "5y",
                            "10y",
                            "ytd",
                            "max",
                        ],
                    },
                    "timestamp": [1672756200, 1672842600],
                    "indicators": {
                        "quote": [
                            {
                                "close": [125.06999969482422, 126.36000061035156],
                                "volume": [112117500, 89113600],
                                "open": [130.27999877929688, 126.88999938964844],
                                "high": [130.89999389648438, 128.66000366210938],
                                "low": [124.16999816894531, 125.08000183105469],
                            }
                        ],
                        "adjclose": [
                            {"adjclose": [123.47061920166016, 124.74411010742188]}
                        ],
                    },
                }
            ],
            "error": None,
        }
    }


@patch("src.fetch.send_request")
def test_fetch_historical_data(mock_send_request, historical_data):
    mock_send_request.return_value = historical_data
    df = fetch_historical_data(
        symbol="AAPL", start_date=datetime(2023, 1, 3), end_date=datetime(2023, 1, 5)
    )
    assert df.shape == (2, 6)
    assert df["date"].tolist() == [
        datetime(2023, 1, 3, hour=14, minute=30),
        datetime(2023, 1, 4, hour=14, minute=30),
    ]
