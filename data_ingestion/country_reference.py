"""
data_ingestion/country_reference.py
Author: 
    Charles Chan, Hsueh-i Lu, Rui Pan, Yaheng Wang, Yigang Zhou, Jiaqi Song

Description: 
    The script contains crawl_country_code function to crawl data from https://countrycode.org/.

Import by:
    data_ingestion/__init__.py

Import:
    crawl_country_code_ref from base.py
"""

from .base import crawl_country_code_ref

"""
Function:
    crawl_country_code
Purpose:
    Use beautifulsoup to scrape the country referennce.
Inputs:
    :params: home_dir -- the home directory for the function to find the right directory to save data
Output:
    a csv saved in the data directory.
"""
def crawl_country_code(home_dir):
    url = "https://countrycode.org/"
    crawl_country_code_ref(url, f"{home_dir}/data/country_code/country_code_reference.csv")

# Test code
if __name__ == "__main__":
    url = "https://countrycode.org/"
    crawl_country_code_ref(url, "../data/country_code/country_code_reference.csv")