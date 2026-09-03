# Extracting and Visualizing Stock Data

This project extracts historical stock price data for **Tesla (TSLA)** and
**GameStop (GME)** using [yfinance](https://pypi.org/project/yfinance/),
scrapes their quarterly revenue data from web pages using
[BeautifulSoup](https://pypi.org/project/beautifulsoup4/), and visualizes
share price against revenue over time using Matplotlib.

## What it does

1. Pulls Tesla's full historical stock price data via `yfinance`.
2. Scrapes Tesla's quarterly revenue data from an HTML page.
3. Pulls GameStop's full historical stock price data via `yfinance`.
4. Scrapes GameStop's quarterly revenue data from an HTML page.
5. Plots Tesla's share price and revenue history side by side.
6. Plots GameStop's share price and revenue history side by side.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python stock_revenue_dashboard.py
```

This prints a preview of each stock/revenue DataFrame to the console and
opens two Matplotlib figures (Tesla and GameStop), each showing historical
share price on top and historical revenue below.

## Files

- `stock_revenue_dashboard.py` — main script containing all data
  extraction, scraping, and plotting logic.
- `requirements.txt` — Python dependencies.

## Notes

- The plotting function (`make_graph`) filters data up to `2021-06-14`
  (stock price) and `2021-04-30` (revenue) to match the original lab's
  scope.
- This project was originally developed as part of an IBM Data Engineering
  / Data Science course lab on extracting and visualizing stock data.
