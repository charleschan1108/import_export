import pandas as pd
import numpy as np
from utils import get_latest_file

def pct_chg_and_merge(df, measure):
    # pivot data and apply pct_change
    pivot = df.pivot(index = "TIME", columns = "LOCATION", values = "Value")
    pivot = pivot.pct_change(fill_method = None).ffill()
    latest_chg = pivot.iloc[-1].to_frame()


    tmp = df[df["TIME"] == latest_chg.columns[0]].set_index("LOCATION")["Value"]
    latest_chg[f"{measure}"] = tmp
    latest_chg.rename(columns = {latest_chg.columns[0]: f"{measure}Change"}, inplace = True)

    return latest_chg

def process_unemployment():
    # get latest file
    directory = "../data/unemployment"
    path = get_latest_file(directory)

    # Read & filter data
    df = pd.read_csv(path, low_memory = False)
    df = df[df["SUBJECT"] == "TOT"]

    # Split into quarterly and yearly
    q_df = df[df["TIME"].str.contains("-Q[1-4]")]
    y_df = df[df["TIME"].str.contains("^[0-9]{4}$")]

    q_chg = pct_chg_and_merge(q_df, "QuarterlyUnemploymentRate")
    y_chg = pct_chg_and_merge(y_df, "YearlyUnemploymentRate")

    # save
    q_chg.to_csv("../insights/unemployment_qoq/latest.csv", header = True, index = True)
    y_chg.to_csv("../insights/unemployment_yoy/latest.csv", header = True, index = True)

if __name__ == "__main__":
    process_unemployment()


