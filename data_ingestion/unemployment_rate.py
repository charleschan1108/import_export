"""
gdp.py
Author: 
    Charles Chan, Hsueh-i Lu, Rui Pan, Yaheng Wang, Yigang Zhou, Jiaqi Song

Description: 
    The script contains download_unemployment_rate function to crawl 
    unemployment rate data for each country from https://data.oecd.org/unemp/unemployment-rate.htm.

Import by:
    data_ingestion/__init__.py

Import:
    download_quarterly_oecd_data from base.py
"""

import os
from .base import download_quarterly_oecd_data

"""
Function:
    download_unemployment_rate
Purpose:
    Use selenium to download unemployment rate data from oecd.
Inputs:
    :params: home_dir -- the home directory for the function to find the right directory to save data
Output:
    a csv saved in the data directory.
"""
def download_unemployment_rate(home_dir):
    url = "https://data.oecd.org/unemp/unemployment-rate.htm"   
    data_directory = os.path.join(home_dir, "data/unemployment")
    download_quarterly_oecd_data(url, home_dir, data_directory)
    return

if __name__ == "__main__":
    download_unemployment_rate()