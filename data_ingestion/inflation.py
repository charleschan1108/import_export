from base import crawl_trading_econ_data
from datetime import datetime

if __name__ == "__main__":
    # Monthly
    url = "https://tradingeconomics.com/country-list/inflation-rate-mom?continent=world"
    today_date = datetime.now().strftime("%Y%m%d")
    crawl_trading_econ_data(url, f"../data/inflation_mom/{today_date}.csv")

    # Yearly
    url = "https://tradingeconomics.com/country-list/inflation-rate?continent=world"
    today_date = datetime.now().strftime("%Y%m%d")
    crawl_trading_econ_data(url, f"../data/inflation_yoy/{today_date}.csv")

    



    