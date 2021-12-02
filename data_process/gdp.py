"""
data_process/gdp.py
Author: 
    Charles Chan, Hsueh-i Lu, Rui Pan, Yaheng Wang, Yigang Zhou, Jiaqi Song

Description: 
    The script contains process_gdp function to process quarter gdp data.

Import by:
    data_process/__init__.py

Import:
    assign_rank from utils.py
    get_country_iso_code from utils.py
    get_latest_file from utils.py
"""

import pandas as pd
import numpy as np

from .utils import get_latest_file
from .utils import get_country_iso_code
from .utils import assign_rank

"""
Function:
    process_gdp
Purpose:
    Read csv stored at data/gdp and compute the rate of change of gdp quarterly and yearly.
    Then, assign rank according to the rate of change.
Inputs:
    :params: home_dir -- the home directory for the function to find the right directory to save data
Output:
    a csv saved in the insights/gdp directory.
"""
def process_gdp(home_dir):
    directory = f"{home_dir}/data/gdp"
    path = get_latest_file(directory)

    # load and filter df
    df = pd.read_csv(path)
    df = df[(df['MEASURE'] == 'IDX') & (df['SUBJECT'] == 'VOLIDX')]
    df = df[df["TIME"].str.contains("-Q")]

    # Take log for convenience in calculating percentage change
    df["Value"] = np.log(df["Value"])

    # pivot and apply diff
    pivot = df.pivot(index = "TIME", columns = "LOCATION", values = "Value")
    latest_chg = pivot.diff().ffill()

    # get QoQ and YoY change
    q_chg = latest_chg.iloc[-1]
    y_chg = latest_chg.iloc[-4:].sum()

    chg = pd.concat([q_chg, y_chg], axis = 1)\
            .rename(columns = {q_chg.name: "QuarterlyGdpChange", 0: "YearlyGdpChange"})

    # add back index value
    chg["QGDP"] = np.exp(pivot.ffill().iloc[-1])
    
    # import country reference
    country_ref = get_country_iso_code()

    # Change iso code to country name
    chg = chg.merge(country_ref, right_index = True, left_index = True, how = "inner").fillna(0.)
    chg.set_index("Country", inplace = True)

    # Assign rank
    for column in chg.columns:
        chg[f"{column}Rank"] = assign_rank(chg[column], "descending")

    # save gdp
    chg.to_csv(f"{home_dir}/insights/gdp/latest.csv", header = True, index = True)

# if __name__ == "__main__":
#     process_gdp()