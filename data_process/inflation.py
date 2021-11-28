import pandas as pd
import numpy as np

from .utils import get_latest_file
from .utils import assign_rank

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
    