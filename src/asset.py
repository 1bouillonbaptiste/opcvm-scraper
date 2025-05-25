"""Define the report module."""

import dataclasses
from datetime import datetime, timedelta

import pandas as pd

from src.fetch import get_symbol_from_isin, fetch_historical_data
from src.metrics import (
    calculate_volatility,
    calculate_max_drawdown,
    calculate_performance,
)


@dataclasses.dataclass
class AssetSummary:
    """Store metrics for an asset."""

    volatility: float
    max_drawdown: float
    performance: float

    def to_dict(self):
        return dataclasses.asdict(self)


def summarize_fluctuations(fluctuations: pd.DataFrame) -> AssetSummary:
    """Calculate historical metrics for fluctuations."""
    return AssetSummary(
        volatility=calculate_volatility(fluctuations),
        max_drawdown=calculate_max_drawdown(fluctuations),
        performance=calculate_performance(fluctuations),
    )


def summarize_asset(isin: str) -> dict[str, dict[str, float]]:
    """Calculate historical metrics for an asset."""

    today_date = datetime.today()
    dataframe = fetch_historical_data(
        symbol=get_symbol_from_isin(isin),
        start_date=today_date - timedelta(days=365 * 3),
        end_date=today_date,
    )
    historical_metrics = {
        "3 years": summarize_fluctuations(
            fluctuations=dataframe[
                dataframe["date"] > today_date - timedelta(days=365 * 3)
            ]
        ).to_dict(),
        "1 year": summarize_fluctuations(
            fluctuations=dataframe[dataframe["date"] > today_date - timedelta(days=365)]
        ).to_dict(),
        "3 months": summarize_fluctuations(
            fluctuations=dataframe[
                dataframe["date"] > today_date - timedelta(days=30 * 3)
            ]
        ).to_dict(),
        "this year": summarize_fluctuations(
            fluctuations=dataframe[
                dataframe["date"]
                > datetime(year=today_date.date().year, month=1, day=1)
            ]
        ).to_dict(),
    }

    return historical_metrics
