import requests
from bs4 import BeautifulSoup

from .Exceptions import *


def get_stock_price(ticker: str, tickerType: str = "stock"):
    tickertypes = ["stock", "crypto"]
    tickerType = tickerType.lower()
    if tickerType not in tickertypes:
        InvalidTickerTypeError(f"Could not find {tickerType} ticker. Valid ticker types are {tickertypes}")

    ticker = ticker.capitalize()

    if tickerType == "stock":
        url = f"https://www.google.com/finance/quote/{ticker}:NASDAQ"

        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        try:
            return float(soup.find_all("div", class_="YMlKec fxKbKc")[0].string.replace("$", "").replace(",", ""))
        except IndexError:
            return float(soup.find_all("div", class_="YMlKec fxKbKc").string.replace("$", "").replace(",", ""))
        except AttributeError:
            if type == "stock":
                raise StockNotFoundError(
                    f"Could not find stock {ticker}. Did you mean to say crypto? Then set the type argument to crypto")
    elif tickerType == "crypto":
        url = f"https://www.google.com/finance/quote/{ticker}-USD"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        try:
            return float(soup.find_all("div", class_="YMlKec fxKbKc")[0].string.replace("$", "").replace(",", ""))
        except IndexError:
            return float(soup.find_all("div", class_="YMlKec fxKbKc").string.replace("$", "").replace(",", ""))
        except AttributeError:
            if type == "stock":
                raise StockNotFoundError(
                    f"Could not find stock {ticker}. Did you mean to say crypto? Then set the type argument to crypto")
