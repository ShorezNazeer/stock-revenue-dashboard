"""
Extracting and Visualizing Stock Data
--------------------------------------
Extracts Tesla (TSLA) and GameStop (GME) historical stock price data via
yfinance, scrapes their quarterly revenue data via BeautifulSoup, and plots
share price vs. revenue for each company.
"""

import warnings

import matplotlib.pyplot as plt
import pandas as pd
import requests
import yfinance as yf
from bs4 import BeautifulSoup

# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)


def make_graph(stock_data, revenue_data, stock):
    """
    Plot historical share price and historical revenue for a given stock.

    Parameters
    ----------
    stock_data : pd.DataFrame
        Must contain 'Date' and 'Close' columns.
    revenue_data : pd.DataFrame
        Must contain 'Date' and 'Revenue' columns.
    stock : str
        Name of the stock, used in plot titles.
    """
    stock_data_specific = stock_data[stock_data.Date <= "2021-06-14"]
    revenue_data_specific = revenue_data[revenue_data.Date <= "2021-04-30"]

    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    # Stock price
    axes[0].plot(
        pd.to_datetime(stock_data_specific.Date),
        stock_data_specific.Close.astype("float"),
        label="Share Price",
        color="blue",
    )
    axes[0].set_ylabel("Price ($US)")
    axes[0].set_title(f"{stock} - Historical Share Price")

    # Revenue
    axes[1].plot(
        pd.to_datetime(revenue_data_specific.Date),
        revenue_data_specific.Revenue.astype("float"),
        label="Revenue",
        color="green",
    )
    axes[1].set_ylabel("Revenue ($US Millions)")
    axes[1].set_xlabel("Date")
    axes[1].set_title(f"{stock} - Historical Revenue")

    plt.tight_layout()
    plt.show()


def scrape_revenue_table(url):
    """
    Scrape a quarterly revenue table (Date, Revenue columns) from a page
    containing a <tbody> table, and return it as a cleaned DataFrame.
    """
    html_data = requests.get(url).text
    soup = BeautifulSoup(html_data, "html.parser")

    revenue = pd.DataFrame(columns=["Date", "Revenue"])
    for row in soup.find("tbody").find_all("tr"):
        col = row.find_all("td")
        date = col[0].text
        rev = col[1].text
        revenue = pd.concat(
            [revenue, pd.DataFrame({"Date": [date], "Revenue": [rev]})],
            ignore_index=True,
        )

    # Clean the Revenue column: strip '$' and ',' and drop empty/null rows
    revenue["Revenue"] = revenue["Revenue"].str.replace(",|\\$", "", regex=True)
    revenue.dropna(inplace=True)
    revenue = revenue[revenue["Revenue"] != ""]

    return revenue


# ---------------------------------------------------------------------------
# Question 1: Use yfinance to extract Tesla stock data
# ---------------------------------------------------------------------------
tesla = yf.Ticker("TSLA")
tesla_data = tesla.history(period="max")
tesla_data.reset_index(inplace=True)
print("Tesla stock data (head):")
print(tesla_data.head())

# ---------------------------------------------------------------------------
# Question 2: Use webscraping to extract Tesla revenue data
# ---------------------------------------------------------------------------
tesla_revenue_url = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
)
tesla_revenue = scrape_revenue_table(tesla_revenue_url)
print("\nTesla revenue data (tail):")
print(tesla_revenue.tail(5))

# ---------------------------------------------------------------------------
# Question 3: Use yfinance to extract GameStop stock data
# ---------------------------------------------------------------------------
GameStop = yf.Ticker("GME")
gme_data = GameStop.history(period="max")
gme_data.reset_index(inplace=True)
print("\nGameStop stock data (head):")
print(gme_data.head())

# ---------------------------------------------------------------------------
# Question 4: Use webscraping to extract GameStop revenue data
# ---------------------------------------------------------------------------
gme_revenue_url = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
)
gme_revenue = scrape_revenue_table(gme_revenue_url)
print("\nGameStop revenue data (tail):")
print(gme_revenue.tail(5))

# ---------------------------------------------------------------------------
# Question 5: Plot Tesla stock graph
# ---------------------------------------------------------------------------
make_graph(tesla_data, tesla_revenue, "Tesla")

# ---------------------------------------------------------------------------
# Question 6: Plot GameStop stock graph
# ---------------------------------------------------------------------------
make_graph(gme_data, gme_revenue, "GameStop")
