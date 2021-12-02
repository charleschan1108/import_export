"""
app/utils.py
Author: 
    Charles Chan, Hsueh-i Lu, Rui Pan, Yaheng Wang, Yigang Zhou, Jiaqi Song

Description: 
    This script here is to store all util functions to be used in app module.

Import by:
    app/app.py
"""

import pandas as pd
import os
import numpy as np

"""
Function:
    get_latest_file
Purpose:
    It is used to find the latest file in the data directory
Inputs:
    :param: directory -- a directory to search for the latest file
Output:
    The path name of the latest file in the given directory
"""
def get_latest_file(directory):
    paths = os.listdir(directory)
    return os.path.join(directory, max(paths))

"""
Function:
    get_trade_partner
Purpose:
    Read the latest file stored at data/trade_partner directory and
    return the trade partner and goods reference (country, top exported/imported goods and 
    top export/import partners) table in the form of pandas data frame
Inputs:
    Nil
Output:
    trade profile reference table.
"""
def get_trade_partner():
    cur_dir = os.path.dirname(__file__)
    path = get_latest_file(f"{cur_dir}/../data/trade_partner")
    df = pd.read_csv(path)
    df.rename(columns = {"Country name": "Country"}, inplace = True)

    for column in df.columns:
        df[column] = df[column].apply(lambda x: x.replace("USA", "United States").replace(">", ""))

    return df


"""
Function:
    assign_rank
Purpose:
    Assign rank to a series of data. The function has two mode, ascending or descending,
    ascending rank means the lower the value, the higher the rank
    descending rank means the higher the value, the higher the rank
    Two mode is needed because some measures is lower the better (e.g. unemployment rate)
    Some is higher the better (e.g. net trade growth rate)
Inputs:
    :param: series -- The series to compute the rank for each entry
    :param: order -- ascending/descending
Output:
    return a series of rank
"""
def assign_rank(series, order):
    """
        Parameters
        :param: series -- numpy array or pandas series
        :param: order -- ascending/descending. ascending means the smaller the higher rank,
                        descending means the larger the higher rank

    """
    argsort = np.argsort(series.values)
    rank = np.zeros_like(argsort)
    res = np.arange(argsort.shape[0])
    res = res if order == "ascending" else res[::-1]
    rank[argsort] = res

    return rank + 1

"""
Function:
    get_country_iso_code
Purpose:
    Read the country_code_reference.csv stored in data/country_code and
    return the country reference (country code and name mapping) table 
    in the form of pandas data frame
Inputs:
    Nil
Output:
    Country code reference table.
"""
def get_country_iso_code():
    cur_dir = os.path.dirname(__file__)
    df = pd.read_csv(f"{cur_dir}/../data/country_code/country_code_reference.csv")
    df = df.drop_duplicates(["Country", "exdIso"])
    return df.set_index("exdIso")["Country"]

if __name__ == "__main__":
    df = get_trade_partner()
    print(df)
    print(df.columns)