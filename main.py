import argparse
import os

import warnings
warnings.simplefilter(action='ignore')

from data_ingestion import download_trade_data
from data_ingestion import download_unemployment_rate
from data_ingestion import scrape_trade_partners
from data_ingestion import crawl_inflation_data
from data_ingestion import download_gdp
from data_ingestion import download_covid_data

from data_process import process_trade
from data_process import process_covid
from data_process import process_gdp
from data_process import process_inflation
from data_process import process_unemployment

from app import app
from config import weighting

# Main process
# refresh data or not
# if refresh & process
# display

def parse_args():
    parser = argparse.ArgumentParser(description = "Import/Export trade recommender")
    parser.add_argument("--refresh", default=0, help = "Whether to re-crawl and re-process data.", type = int)
    parser.add_argument("--topn", default = 10, help = "Number of result to return.", type = int)
    parser.add_argument("--equal_weight", default = 0, help = "Weighting of different indicators.", type = int)
    parser.add_argument("--country", default = None, help = "Country to look up.", type=str)

    return parser.parse_args()

def main():
    # parse argument
    args = parse_args()
    refresh = args.refresh

    # get home dir
    home_dir = os.getcwd()

    # Preprocess
    if bool(int(refresh)):
        # Crawl
        print("Crawling trade data...")
        download_trade_data(home_dir)

        print("Crawling unemployment data...")
        download_unemployment_rate(home_dir)

        print("Crawling trade partner data...")
        scrape_trade_partners(home_dir)

        print("Crawling inflation data...")
        crawl_inflation_data(home_dir)

        print("Crawling gdp data...")
        download_gdp(home_dir)

        print("Crawling covid data...")
        download_covid_data(home_dir)

        # Process
        print("Processing trade data..")
        process_trade(home_dir)

        print("processing unemployment daata..")
        process_unemployment(home_dir)

        print("processing inflation data..")
        process_inflation(home_dir)

        print("processing gdp data..")
        process_gdp(home_dir)

        print("processing covid data..")
        process_covid(home_dir)

    # Display
    if bool(int(args.equal_weight)):
        app(home_dir, perspective_country=args.country, topn = int(args.topn))
    else:
        app(home_dir, perspective_country=args.country,
            weighting = weighting, topn = int(args.topn))

if __name__ == "__main__":
    main()