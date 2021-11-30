"""
inflation.py
Author: 
    Charles Chan, Hsueh-i Lu, Rui Pan, Yaheng Wang, Yigang Zhou, Jiaqi Song

Description: 
    The script contains crawl_inflation_data function to crawl inflation rate data from https://tradingeconomics.com.

Import by:
    data_ingestion/__init__.py

Import:
    crawl_trading_econ_data from base.py
"""

from .base import crawl_trading_econ_data
from datetime import datetime
import os

cur_dir = os.path.dirname(__file__)

"""
Function:
    crawl_inflation_data
Purpose:
    Use beautifulsoup to scrape the month of month and year of year inflation data for each country.
Inputs:
    :params: home_dir -- the home directory for the function to find the right directory to save data
Output:
    a csv saved in the data directory.
"""
def crawl_inflation_data(home_dir):
    # Monthly
    url = "https://tradingeconomics.com/country-list/inflation-rate-mom?continent=world"
    today_date = datetime.now().strftime("%Y%m%d")
    crawl_trading_econ_data(url, f"{home_dir}/data/inflation_mom/{today_date}.csv")

    # Yearly
    url = "https://tradingeconomics.com/country-list/inflation-rate?continent=world"
    today_date = datetime.now().strftime("%Y%m%d")
    crawl_trading_econ_data(url, f"{home_dir}/data/inflation_yoy/{today_date}.csv")

if __name__ == "__main__":
    crawl_inflation_data()


    



    