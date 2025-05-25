import pandas as pd
import numpy as np


def calculate_max_drawdown(fluctuations: pd.DataFrame) -> float:
    """Calculate the biggest loss of market data."""
    if len(fluctuations) < 2:
        raise ValueError("Not enough data to calculate drawdown.")

    drawdown = [
        np.max(fluctuations["high"][: ii + 1]) - fluctuations["low"][ii]
        for ii in range(1, len(fluctuations))
    ]
    return round(float(np.max(drawdown)), 3)


def calculate_volatility(fluctuations: pd.DataFrame) -> float:
    """Calculate the volatility (or standard-deviation) of market data returns."""
    if len(fluctuations) < 2:
        raise ValueError("Not enough data to calculate volatility.")

    returns = fluctuations["close"].pct_change()
    return round(float(returns.std()), 3)
