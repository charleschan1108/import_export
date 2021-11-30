"""
__init__.py
Author: 
    Charles Chan, Hsueh-i Lu, Rui Pan, Yaheng Wang, Yigang Zhou, Jiaqi Song

Description: 
    Contains all function in this module for importing by other modules

Import by:
    ../main.py

"""

from .unemployment_rate import download_unemployment_rate
from .trade import download_trade_data
from .trade_partner import scrape_trade_partners
from .inflation import crawl_inflation_data
from .gdp import download_gdp
from .covid import download_covid_data
from .country_reference import crawl_country_code
from .covid_death import idx1
from .indexMundi_specified import indexMundiGetDataFrame
from .WebScraping_GDP_in_Current_Price import getGdpData
