# opcvm-scrapper

OPCVM scrapping library

## Installation

Requires [pyenv](https://github.com/pyenv/pyenv) to be installed.

You can install the package by running the following commands

```bash
pyenv virtualenv 3.10.14 opcvm-scraper
pyenv activate opcvm-scraper
```

Then the bellow command will automatically install the `opcvm-scraper` project.

```bash
make setup
```

## Usage

You can summarize an asset performance by running :

```python
from src.asset import summarize_asset

isin = "IE0002XZSHO1"
asset_summary = summarize_asset(isin)
```

Which gives you a dictionary containing metrics for various timeframes.

For `IE0002XZSHO1` at `2025-05-25`, the summary is saved in the `IE0002XZSHO1.json` file that contains :

```txt
              3 years  1 year  3 months  this year
volatility      0.011   0.011     0.018      0.015
max_drawdown    0.239   0.239     0.224      0.239
performance     0.077   0.061    -0.067     -0.069
```

## Formula

The **volatility** is the standard-deviation of daily returns.

The **max-drawdown** is the highest drop in percentage from the previous high.

The **performance** is the total return from the starting date.


## Limitations

Under the hood, we scrap historical data from Yahoo Finance.

The lowest available timeframe for old data is daily, which is enough for this project.

It is not possible to specify a custom date range for now. Could be added with little effort, though.
