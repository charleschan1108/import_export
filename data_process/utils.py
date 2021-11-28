import os
import pandas as pd
import numpy as np

def get_latest_file(directory):
    paths = os.listdir(directory)
    return os.path.join(directory, max(paths))

def get_country_iso_code():
    cur_dir = os.path.dirname(__file__)
    df = pd.read_csv(f"{cur_dir}/../data/country_code/country_code_reference.csv")
    df = df.drop_duplicates(["Country", "exdIso"])
    return df.set_index("exdIso")["Country"]

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