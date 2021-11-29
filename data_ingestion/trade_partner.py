import re
import os
from bs4 import BeautifulSoup as bs
import requests as req
import pandas as pd
# from .CountryNameUtil import countryNameHandle

from datetime import datetime

# Function to get data of specified country from https://www.seair.co.in/global-trade-data.aspx
# CountryName means name of country, check Products&Partners_Data.xlsx for available country
# Return a DataFrame, 1st column is name of country, 2nd is Top exported products,
# 3rd is Top export partners, 4th is Top imported products, 5th is Top import partners
# Caution: not all countries have all kind of data, check Products&Partners_Data.xlsx for more detail
def product_partner_scraper():    # countryName
    # Here I do a little examine of CountryNameUtil, if not needed, comment it and edit line 43
    # countryName = cnu.countryNameHandle(countryName)
    url = "https://www.seair.co.in/global-trade-data.aspx"
    r = req.get(url, timeout=10)
    demo = r.text  # server respond

    """
    demo is content of html
    """
    soup = bs(demo, "html.parser")
    country_list = soup.find('ul', {'class': 'gtd_maplist'})
    country_block = country_list.children  # should be div block
    country_names = []  # list of country names
    export_urls = []  # list of exported urls
    import_urls = []  # list of imported urls
    for i in country_block:  # get country name
        name = (re.findall(r'.*<h5>(.*)<b>', str(i.find('h5'))))
        if len(name) > 0:
            country_names.append(name[0].strip())
    urls_block = soup.find_all('div', {'class': 'btncolarea'})
    for i in urls_block:  # get all export and import urls
        urls = re.findall(r'.*href="(.*)">', str(i))
        export_urls.append(urls[0])
        import_urls.append(urls[1])

    df = pd.DataFrame(columns=['Country name', 'Top exported products', 'Top export partners',
                               'Top imported products', 'Top import partners'])  # use DataFrame to quickly build data

    for i in range(len(country_names)):
        # CountryNameUtil test
        # if cnu.countryNameHandle(countryName[i]) == countryName:
        ex_top_products = []  # list of exported products
        ex_top_partners = []  # list of exported partners
        # try to concat exported urls
        if export_urls[i] != 'javascript:void(0);':
            ex_url = "https://www.seair.co.in" + export_urls[i]
            # a new website, for export info
            print(ex_url)
            ex_r = req.get(ex_url, timeout=10)
            ex_demo = ex_r.text
            ex_soup = bs(ex_demo, "html.parser")
            pattern_ex_product = re.compile('.*Top Most Exported Products.*')
            ex_product_pos = ex_soup.find(text=pattern_ex_product)
            if ex_product_pos is not None:
                ex_product_div = ex_product_pos.parent.parent
                product_list = ex_product_div.find('ul').stripped_strings  # top most exported products
                if product_list is not None:
                    for x in product_list:
                        product_str = x #.text.strip()
                        if product_str != '':
                            ex_top_products.append(product_str)

            pattern_ex_partner = re.compile('.*Top Export Partners.*')
            ex_partner_pos = ex_soup.find(text=pattern_ex_partner)
            if ex_partner_pos is not None:
                ex_partner_div = ex_partner_pos.parent.parent
                partner_list = ex_partner_div.find('ul').stripped_strings  # top most exported partners
                if partner_list is not None:
                    for x in partner_list:
                        partner_str = x #.text.strip()
                        if partner_str != '':
                            ex_top_partners.append(partner_str)

        im_top_products = []  # list of imported products
        im_top_partners = []  # list of exported partners
        # try to concat imported urls
        if import_urls[i] != 'javascript:void(0);':
            im_url = "https://www.seair.co.in" + import_urls[i]
            # a new website, for import info
            print(im_url)
            im_r = req.get(im_url, timeout=10)
            im_demo = im_r.text
            im_soup = bs(im_demo, "html.parser")

            pattern_im_product = re.compile('.*Top Most Imported Products.*')
            im_product_pos = im_soup.find(text=pattern_im_product)
            if im_product_pos is not None:
                im_product_div = im_product_pos.parent.parent
                product_list = im_product_div.find('ul').stripped_strings  # top most imported products
                if product_list is not None:
                    for x in product_list:
                        product_str = x #.text.strip()
                        if product_str != '':
                            im_top_products.append(product_str)

            pattern_im_partner = re.compile('.*Top Import Partners.*')
            im_partner_pos = im_soup.find(text=pattern_im_partner)
            if im_partner_pos is not None:
                im_partner_div = im_partner_pos.parent.parent
                partner_list = im_partner_div.find('ul').stripped_strings  # top most imported partners
                if partner_list is not None:
                    for x in partner_list:
                        partner_str = x #.text.strip()
                        if partner_str != '':
                            im_top_partners.append(partner_str)

        df = df.append({'Country name': country_names[i],
                        'Top exported products': ex_top_products,
                        'Top export partners': ex_top_partners,
                        'Top imported products': im_top_products,
                        'Top import partners': im_top_partners
                        }, ignore_index=True)
        # return df
    return df

def scrape_trade_partners(home_dir):
    today_date = datetime.now().strftime("%Y%m%d")
    df = product_partner_scraper()
    df.to_csv(f"{home_dir}/data/trade_partner/{today_date}.csv", header = True, index = False)

# if __name__ == "__main__":
#     scrape_trade_partners()
