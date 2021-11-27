import os
from base import download_quarterly_oecd_data

def download_trade_data():
    url = "https://data.oecd.org/trade/trade-in-goods-and-services.htm#indicator-chart"
    data_directory = os.path.join(os.path.dirname(os.getcwd()), "data/trade")
    download_quarterly_oecd_data(url, data_directory)
    return
    
if __name__ == "__main__":
    download_trade_data()