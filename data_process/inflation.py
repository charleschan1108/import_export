import pandas as pd
import numpy as np

from utils import get_latest_file

def _process_inflation(dir_basename):
    """
        Input: directory basename
        Output: None
        Purpose: process the latest file of inflation data from data/{dir_basename}
    """

    # get latest mom inflation csv
    directory = f"../data/{dir_basename}"
    path = get_latest_file(directory)

    # read csv
    df = pd.read_csv(path)

    # Assign rank
    # rank = np.argsort(df["Last"].values) + 1
    # df["rank"] = rank

    # save dataframe
    df.to_csv(f"../insights/{dir_basename}/latest.csv")

def process_inflation():
    # process MoM inflation
    process_inflation("inflation_mom")

    # process YoY inflation
    process_inflation("inflation_yoy")

if __name__ == "__main__":
    process_inflation()
    