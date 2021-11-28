import pandas as pd
import os
import numpy as np

def get_latest_file(directory):
    paths = os.listdir(directory)
    return os.path.join(directory, max(paths))

def get_trade_partner():
    cur_dir = os.path.dirname(__file__)
    path = get_latest_file(f"{cur_dir}/../data/trade_partner")
    df = pd.read_csv(path)
    df.rename(columns = {"Country name": "Country"}, inplace = True)

    for column in df.columns:
        df[column] = df[column].apply(lambda x: x.replace("USA", "United States"))

    return df

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

if __name__ == "__main__":
    df = get_trade_partner()
    print(df)
    print(df.columns)