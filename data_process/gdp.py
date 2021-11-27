import pandas as pd
import numpy as np

from utils import get_latest_file

def process_gdp():
    directory = "../data/gdp"
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
    
    # save gdp
    chg.to_csv("../insights/gdp/latest.csv", header = True, index = True)

if __name__ == "__main__":
    process_gdp()