"""
data_process/inflation.py
Author: 
    Charles Chan, Hsueh-i Lu, Rui Pan, Yaheng Wang, Yigang Zhou, Jiaqi Song

Description: 
    The script contains process_inflation and _process_inflation functions to 
    combine month of month and year of year inflation.

Import by:
    data_process/__init__.py

Import:
    assign_rank from utils.py
    get_latest_file from utils.py
"""

import pandas as pd
import numpy as np

from .utils import get_latest_file
from .utils import assign_rank

"""
Function:
    _process_inflation
Purpose:
    process the latest file of inflation data from data/{dir_basename}, where dir_basename
    can inflation_mom or inflation_yoy.
    Then assign rank for the inflation rate.
Inputs:
    :params: home_dir -- the home directory for the function to find the right directory to save data
    :params: dir_basename -- inflation_yoy or inflation_mom
    :params: measure -- Prefix to add to the column name of the dataframe to be returned
Output:
    A pandas data frame that contains inflation data
"""
def _process_inflation(home_dir, dir_basename, measure):
    """
        Input: directory basename
        Output: None
        Purpose: process the latest file of inflation data from data/{dir_basename}
    """

    # get latest mom inflation csv
    directory = f"{home_dir}/data/{dir_basename}"
    path = get_latest_file(directory)

    # read csv
    df = pd.read_csv(path)

    # reformat
    df.rename(columns = {"Last": f"{measure}Inflation"}, inplace = True)
    df[f"{measure}Inflation"] = df[f"{measure}Inflation"] / 100
    df.set_index("Country", inplace = True)
    
    return df[f"{measure}Inflation"]

"""
Function:
    process_inflation
Purpose:
    Run _process_inflation for inflation_mom and inflation_yoy and combine the two before saving
    as csv
Inputs:
    :params: home_dir -- the home directory for the function to find the right directory to save data
Output:
    a csv saved in the insights/gdp directory.
"""
def process_inflation(home_dir):
    # process MoM inflation
    mom = _process_inflation(home_dir, "inflation_mom", "Quarterly")

    # process YoY inflation
    yoy = _process_inflation(home_dir, "inflation_yoy", "Yearly")

    # combine
    combined = pd.concat([mom, yoy], axis = 1).fillna(0.)

    # assign rank
    for column in combined.columns:
        combined[f"{column}Rank"] = assign_rank(combined[column], "ascending")

    # Save
    combined.to_csv(f"{home_dir}/insights/inflation/latest.csv", header = True, index = True)


# if __name__ == "__main__":
#     process_inflation()
    