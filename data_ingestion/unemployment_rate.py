import os
from base import download_quarterly_oecd_data

def download_unemployment_rate():
    url = "https://data.oecd.org/unemp/unemployment-rate.htm"   
    data_directory = os.path.join(os.path.dirname(os.getcwd()), "data/unemployment")
    download_quarterly_oecd_data(url, data_directory)
    return

if __name__ == "__main__":
    download_unemployment_rate()