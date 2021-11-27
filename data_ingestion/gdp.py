import os
from base import download_quarterly_oecd_data

def download_gdp():
    url = "https://data.oecd.org/gdp/quarterly-gdp.htm"
    data_directory = os.path.join(os.path.dirname(os.getcwd()), "data/gdp")
    download_quarterly_oecd_data(url, data_directory)
    return

if __name__ == "__main__":
    download_gdp()
