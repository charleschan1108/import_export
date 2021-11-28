import os
from .base import download_quarterly_oecd_data

def download_unemployment_rate(home_dir):
    url = "https://data.oecd.org/unemp/unemployment-rate.htm"   
    data_directory = os.path.join(home_dir, "data/unemployment")
    download_quarterly_oecd_data(url, home_dir, data_directory)
    return

if __name__ == "__main__":
    download_unemployment_rate()