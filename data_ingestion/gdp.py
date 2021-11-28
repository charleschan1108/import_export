import os
from .base import download_quarterly_oecd_data

def download_gdp(home_dir):
    url = "https://data.oecd.org/gdp/quarterly-gdp.htm"
    data_directory = os.path.join(home_dir, "data/gdp")
    download_quarterly_oecd_data(url, home_dir, data_directory)
    return

# if __name__ == "__main__":
#     download_gdp()
