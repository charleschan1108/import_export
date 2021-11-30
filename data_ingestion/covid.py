"""
covid.py
Author: 
    Charles Chan, Hsueh-i Lu, Rui Pan, Yaheng Wang, Yigang Zhou, Jiaqi Song

Description: 
    The script contains function to crawl covid data from https://ourworldindata.org

Import by:
    data_ingestion/__init__.py

Import:
    Nil
"""

from selenium import webdriver
import time
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

cur_dir = os.path.dirname(__file__)

def safe_remove_file(path):
    try:
        os.remove(path)
    except:
        pass
    return

"""
Function:
    download_covid_data
Purpose:
    Use selenium perform a chain of actions to download data from owid, that is, first scroll
    down to the bottom and get the DOM to load all the components on the website, then find the 
    buttons lead to the link to download the daily covid data for all countries in the world.
Inputs:
    :params: home_dir -- the home directory for the function to find the right directory to save data
Output:
    a csv saved in the data directory.
"""
def download_covid_data(home_dir):
    url = "https://ourworldindata.org/explorers/coronavirus-data-explorer"
    directory = os.path.join(home_dir, "data/covid")

    # remove file first
    path = os.path.join(directory, "owid-covid-data.csv")
    safe_remove_file(path)

    # set Chrome webdriver options
    # set default directory to data
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : directory}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(f"{home_dir}/chromedriver", chrome_options=options)

    # browse url
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # click download
    WebDriverWait(driver,10).until(
        EC.element_to_be_clickable((By.XPATH,"//li[contains(@class,'tab clickable icon')]"))).click()
    WebDriverWait(driver,10).until(
        EC.element_to_be_clickable((By.XPATH,"//button[@data-track-note='chart-download-csv']"))).click()

    # Give it 30 secs to download
    time.sleep(30)
    driver.close()

if __name__ == "__main__":
    download_covid_data()


