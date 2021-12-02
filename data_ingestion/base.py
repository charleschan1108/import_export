"""
data_ingestion/base.py
Author: 
    Charles Chan, Hsueh-i Lu, Rui Pan, Yaheng Wang, Yigang Zhou, Jiaqi Song

Description: 
    This script here is to store all crawler functions to be used in data_ingestion module.

Import by:
    country_reference.py
    covid.py
    gdp.py
    inflation.py
    trade.py
    unemployment_rate.py
"""


from selenium import webdriver
import time

import urllib3
from bs4 import BeautifulSoup
import pandas as pd
import os

cur_dir = os.path.dirname(__file__)

"""
Function:
    download_quarterly_oecd_data
Purpose:
    Use selenium to perform actions of downloading data from oecd websites as if it is done by a human 
    (i.e. visit the websites and click the buttons to downlaod the data.)
Inputs:
    :param: url -- oecd data url (e.g. https://data.oecd.org/gdp/quarterly-gdp.htm)
    :param: home_dir -- home directroy, where main.py is at. To help finding the chromdriver
    :param: directory -- where to save the data
Output:
    a csv saved in the data directory.
"""
def download_quarterly_oecd_data(url, home_dir, directory):
    # set Chrome webdriver options
    # set default directory to data
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : directory}
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(f"{home_dir}/chromedriver", chrome_options=options)
    
    # browse url
    driver.get(url)

    # click the dropdown menu and click download
    driver.find_element_by_xpath("//span[@class='download-btn-label']").click()
    driver.find_element_by_xpath("//li/a[@class='download-indicator-button']").click()

    time.sleep(30)
    driver.close()

"""
Function:
    reshape_bs4
Purpose:
    When using bs4 to scrape tag td from a html, you will get a list of elements of td tag. 
    This function takes that list and number of columns it supposed to have as arguments, and 
    reshape that list to a list of list with the correct dimensions.
Inputs:
    :param: table -- lists of td tag elements obtained from bs4.find_all("td")
    :param: ncols -- number of columns the table has
Output:
    a reshaped list of lists
"""
def reshape_bs4(table, ncols):
    # reshaping a table
    output = []
    res = []
    count = 0
    for row in table:
        if ((count % ncols) == 0) & (count > 0):
            output.append(res)
            res = []
        
        res.append(row.text.strip())
        count += 1
    return output

"""
Function:
    crawl_table
Purpose:
    To get the table in any website.
Inputs:
    :param: url -- The url that contains a table of interst
    :param: columns -- columns names for the table
Output:
    The table of interest in pandas data frame format.
"""
def crawl_table(url, columns):
    # get html and parse with beautiful soup
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data)

    # parse and reshape into a table
    table = soup.find_all("td")
    output = reshape_bs4(table, len(columns))
    
    # transform into a dataframe
    df = pd.DataFrame(output, columns = columns)
    return df

"""
Function:
    crawl_trading_econ_data
Purpose:
    Use beautifulsoup to scrape the table from trading economics website.
Inputs:
    :param: url -- trading economics url (e.g. https://tradingeconomics.com/country-list/inflation-rate-mom?continent=world)
    :param: savepath -- where to save the data
Output:
    a csv saved in the data directory.
"""
def crawl_trading_econ_data(url, savepath):
    df = crawl_table(url, ["Country", "Last", "Previous", "Reference", "Unit"])
    df.to_csv(savepath, header = True, index =False)

"""
Function:
    crawl_country_code_ref
Purpose:
    Use beautifulsoup to scrape the country referennce.
Inputs:
    :param: url -- url that contains country iso code. (e.g. https://countrycode.org/)
    :param: savepath -- where to save the data
Output:
    a csv saved in the data directory.
"""
def crawl_country_code_ref(url, savepath):
    columns = [
        "Country",
        "Country Code",
        "ISO Code",
        "Population",
        "Area",
        "GDP(USD)"
    ]
    df = crawl_table(url, columns)
    df["Iso"] = df["ISO Code"].apply(lambda x: x.split("/")[0].strip())
    df["exdIso"] = df["ISO Code"].apply(lambda x: x.split("/")[1].strip())
    df.to_csv(savepath, header = True, index =False)





