from base import crawl_country_code_ref



if __name__ == "__main__":
    url = "https://countrycode.org/"
    crawl_country_code_ref(url, "../data/country_code/country_code_reference.csv")