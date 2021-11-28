from selenium.webdriver.common.by import By
from time import sleep,time
import numpy as np
import pandas as pd

"""
getGdpData() function scraps the "GDP in Current Price" table from the website
 (https://knoema.com/nwnfkne/world-gdp-ranking-2020-gdp-by-country-data-and-charts)
return a dataframe storing the table.
"""
def getGdpData(browser):
      
    browser.get('https://knoema.com/nwnfkne/world-gdp-ranking-2020-gdp-by-country-data-and-charts')
    sleep(3)
    
    df = []
    for elems in browser.find_elements(By.CLASS_NAME,'pivot-table'):  #our target is the third table - GDP in Current Price
        rows = []
        col_names = [y.text for y in elems.find_elements(By.XPATH, './/thead/tr/th[@colspan=1]')]
        for tr in elems.find_elements(By.XPATH, './/tbody/tr'):
            country = tr.find_element(By.XPATH, './/th').text
            nums = [td.text for td in tr.find_elements(By.XPATH, './/td[not(@class = "table-cell-with-unit")]')]
            nums.insert(0, country)
            rows.append(nums)
        nprows = np.array(rows)
        col_names.insert(0, "country")
        df = pd.DataFrame(nprows)
        df.columns = col_names
        break  
    browser.close()
    return df
