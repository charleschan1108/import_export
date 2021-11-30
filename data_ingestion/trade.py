"""
trade.py
Author: 
    Charles Chan, Hsueh-i Lu, Rui Pan, Yaheng Wang, Yigang Zhou, Jiaqi Song

Description: 
    The script contains download_trade_data function to download import and export
    trade data from https://data.oecd.org/trade/trade-in-goods.htm#indicator-chart.

Import by:
    data_ingestion/__init__.py

Import:
    download_quarterly_oecd_data from base.py
"""

import os
from .base import download_quarterly_oecd_data

"""
Function:
    download_trade_data
Purpose:
    Use selenium to download import and export trade data from oecd.
Inputs:
    :params: home_dir -- the home directory for the function to find the right directory to save data
Output:
    a csv saved in the data directory.
"""
def download_trade_data(home_dir):
    url = "https://data.oecd.org/trade/trade-in-goods.htm#indicator-chart"
    data_directory = os.path.join(home_dir, "data/trade")
    download_quarterly_oecd_data(url, home_dir, data_directory)
    return
    
if __name__ == "__main__":
    download_trade_data()