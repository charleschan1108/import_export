"""
data_process/trade.py
Author: 
    Charles Chan, Hsueh-i Lu, Rui Pan, Yaheng Wang, Yigang Zhou, Jiaqi Song

Description: 
    The script contains get_rate_of_change and process_trade function to process 
    quarter trade (export/import/net trade) data.

Import by:
    data_process/__init__.py

Import:
    assign_rank from utils.py
    get_country_iso_code from utils.py
    get_latest_file from utils.py
"""

import pandas as pd
import numpy as np

from .utils import assign_rank
from .utils import get_latest_file
from .utils import get_country_iso_code


"""
Function:
    get_rate_of_change
Purpose:
    To transform the raw data by pivoting the table before calculating rate of change for 
    the value of import/export/net trade in goods for each country.
Inputs:
    :params: df -- raw data filtered by subject (exp/imp/ntrade)
    :params: measure -- suffix for the naming of the output in the data frame
    :params: verbose -- whether to print data frame for debugging purposes
Output:
    A pandas data frame that contains rate of change of value of import/export/net trade in goods.
"""
def get_rate_of_change(df, measure, verbose = False):
    pivot = df.pivot(index = "TIME", columns = "LOCATION", values = "Value")
    latest_chg = pivot.pct_change(fill_method = None).ffill()

    if verbose:
        print(latest_chg)

    # quarterly & yearly change
    q_chg = latest_chg.iloc[-1]
    y_chg = (latest_chg.iloc[-1] / latest_chg.iloc[-4] - 1)

    # combine the 2 changes
    chg = pd.concat([q_chg, y_chg], axis = 1)

    # reformat
    chg = chg.rename(columns = {q_chg.name: f"QuarterlyChange{measure}",
                                0: f"YearlyChange{measure}"})

    # add Value
    chg[measure] = df[df["TIME"] == q_chg.name].set_index("LOCATION")["Value"]

    return chg

"""
Function:
    process_trade
Purpose:
    First filter and split the raw data into import_df, export_df and net_df.
    Then apply get_rate_of_change to each of the data frames
    Finally, combine the three data frames and assign rank according to the rate
    of change..
Inputs:
    :params: home_dir -- the home directory for the function to find the right directory to save data
Output:
    a csv saved in the insights/trade directory.
"""
def process_trade(home_dir):
    directory = f"{home_dir}/data/trade"
    path = get_latest_file(directory)
    
    # read and filter data
    df = pd.read_csv(path)
    df = df[df["FREQUENCY"] == "Q"]
    import_df = df[(df["SUBJECT"] == "IMP") & (df["MEASURE"] == "BLN_USD")]
    export_df = df[(df["SUBJECT"] == "EXP") & (df["MEASURE"] == "BLN_USD")]
    net_df = df[(df["SUBJECT"] == "NTRADE") & (df["MEASURE"] == "BLN_USD")]

    # Get rate of change
    import_df = get_rate_of_change(import_df, "IMP")
    export_df = get_rate_of_change(export_df, "EXP")
    net_df = get_rate_of_change(net_df, "NTRADE")

    # add country name
    country_ref = get_country_iso_code()
    
    # Combine
    combined = pd.concat([import_df, export_df, net_df], axis = 1)
    combined = combined.merge(country_ref, left_index=True, right_index = True, how = "inner").fillna(0.)
    combined = combined.set_index("Country")

    # Assign rank
    for column in combined.columns:
        combined[f"{column}Rank"] = assign_rank(combined[column], "descending")
    
    # Save
    combined.to_csv(f"{home_dir}/insights/trade/latest.csv", header = True, index = True)

if __name__ == "__main__":
    process_trade()