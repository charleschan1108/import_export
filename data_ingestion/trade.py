import os
from .base import download_quarterly_oecd_data

def download_trade_data(home_dir):
    url = "https://data.oecd.org/trade/trade-in-goods.htm#indicator-chart"
    data_directory = os.path.join(home_dir, "data/trade")
    download_quarterly_oecd_data(url, home_dir, data_directory)
    return
    
if __name__ == "__main__":
    download_trade_data()