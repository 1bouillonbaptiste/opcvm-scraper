import pandas as pd
import numpy as np


def calculate_max_drawdown(fluctuations: pd.DataFrame) -> float:
    """Calculate the biggest loss of market data."""
    if len(fluctuations) < 2:
        raise ValueError("Not enough data to calculate drawdown.")

    highs = fluctuations["high"].tolist()
    lows = fluctuations["low"].tolist()
    drawdowns = []
    for index in range(len(fluctuations)):
        highest_high = max(highs[: index + 1])
        drawdown = (highest_high - lows[index]) / highest_high
        drawdowns.append(drawdown)
    return round(float(np.max(drawdowns)), 3)


def calculate_volatility(fluctuations: pd.DataFrame) -> float:
    """Calculate the volatility (or standard-deviation) of market data returns."""
    if len(fluctuations) < 2:
        raise ValueError("Not enough data to calculate volatility.")

    returns = fluctuations["close"].pct_change()
    return round(float(returns.std()), 3)


def calculate_performance(fluctuations: pd.DataFrame) -> float:
    """Calculate the performance of market data."""
    if len(fluctuations) < 2:
        raise ValueError("Not enough data to calculate performance.")

    closes = fluctuations["close"].tolist()
    last_close = closes[-1]
    first_close = closes[0]
    return round(float((last_close - first_close) / first_close), 3)
