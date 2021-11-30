"""
gdp.py
Author: 
    Charles Chan, Hsueh-i Lu, Rui Pan, Yaheng Wang, Yigang Zhou, Jiaqi Song

Description: 
    The script contains download_gdp function to crawl gdp data from https://data.oecd.org/gdp/quarterly-gdp.htm.

Import by:
    data_ingestion/__init__.py

Import:
    download_quarterly_oecd_data from base.py
"""
import os
from .base import download_quarterly_oecd_data

"""
Function:
    download_gdp
Purpose:
    Use selenium to download data from oecd.
Inputs:
    :params: home_dir -- the home directory for the function to find the right directory to save data
Output:
    a csv saved in the data directory.
"""
def download_gdp(home_dir):
    url = "https://data.oecd.org/gdp/quarterly-gdp.htm"
    data_directory = os.path.join(home_dir, "data/gdp")
    download_quarterly_oecd_data(url, home_dir, data_directory)
    return

# if __name__ == "__main__":
#     download_gdp()
