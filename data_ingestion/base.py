from selenium import webdriver
import time

import urllib3
from bs4 import BeautifulSoup
import pandas as pd
import os

cur_dir = os.path.dirname(__file__)

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

def crawl_trading_econ_data(url, savepath):
    df = crawl_table(url, ["Country", "Last", "Previous", "Reference", "Unit"])
    df.to_csv(savepath, header = True, index =False)

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





