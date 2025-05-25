import pandas as pd
import pytest
from pytest_cases import parametrize_with_cases

from src.metrics import (
    calculate_max_drawdown,
    calculate_volatility,
    calculate_performance,
)


class CalculateMaxDrawdownCases:
    """Generate cases for `calculate_max_drawdown()`.

    Each case returns:
    - fluctuations as a dataframe
    - expected max drawdown
    """

    def case_uponly(self):
        """Price never goes down."""
        return pd.DataFrame({"high": [1, 2, 3], "low": [1, 2, 3]}), 0.0

    def case_downonly(self):
        """Price never goes up."""
        return pd.DataFrame({"high": [3, 2, 1], "low": [3, 2, 1]}), 2 / 3

    def case_downup(self):
        """Price forms a `V`, dd is the difference between the first and the middle candle."""
        return pd.DataFrame({"high": [5, 4, 3, 4, 5], "low": [3, 2, 1, 2, 3]}), 4 / 5

    def case_updown(self):
        """Price forms a `^`, dd is the difference between the middle and the last candle."""
        return pd.DataFrame({"high": [3, 4, 5, 4, 3], "low": [1, 2, 3, 2, 1]}), 4 / 5

    def case_two_drawdowns(self):
        """Price forms two drawdowns, keep the maximum which is the second one."""
        return pd.DataFrame({"high": [6, 5, 4, 7, 5], "low": [4, 3, 3, 5, 3]}), 4 / 7


@parametrize_with_cases(
    "fluctuations, expected_max_drawdown", cases=CalculateMaxDrawdownCases
)
def test_calculate_max_drawdown(fluctuations, expected_max_drawdown):
    maw_drawdown = calculate_max_drawdown(fluctuations)
    assert maw_drawdown == pytest.approx(expected_max_drawdown, abs=1e-3)


def test_calculate_volatility():
    fluctuations = pd.DataFrame({"close": [1, 2, 3, 2, 1]})
    volatility = calculate_volatility(fluctuations)
    assert volatility == 0.707


def test_calculate_performance():
    fluctuations = pd.DataFrame({"close": [1, 2, 3, 2]})
    performance = calculate_performance(fluctuations)
    assert performance == 1
