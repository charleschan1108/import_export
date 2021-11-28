from .base import crawl_trading_econ_data
from datetime import datetime
import os

cur_dir = os.path.dirname(__file__)

def crawl_inflation_data(home_dir):
    # Monthly
    url = "https://tradingeconomics.com/country-list/inflation-rate-mom?continent=world"
    today_date = datetime.now().strftime("%Y%m%d")
    crawl_trading_econ_data(url, f"{home_dir}/data/inflation_mom/{today_date}.csv")

    # Yearly
    url = "https://tradingeconomics.com/country-list/inflation-rate?continent=world"
    today_date = datetime.now().strftime("%Y%m%d")
    crawl_trading_econ_data(url, f"{home_dir}/data/inflation_yoy/{today_date}.csv")

if __name__ == "__main__":
    crawl_inflation_data()


    



    