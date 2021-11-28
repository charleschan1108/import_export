import pandas as pd
import numpy as np

from .utils import get_latest_file
from .utils import get_country_iso_code
from .utils import assign_rank

def pct_chg_and_merge(df, measure):
    # pivot data and apply pct_change
    pivot = df.pivot(index = "TIME", columns = "LOCATION", values = "Value")
    pivot = pivot.pct_change(fill_method = None).ffill()
    latest_chg = pivot.iloc[-1].to_frame()


    tmp = df[df["TIME"] == latest_chg.columns[0]].set_index("LOCATION")["Value"]
    latest_chg[f"{measure}"] = tmp
    latest_chg.rename(columns = {latest_chg.columns[0]: f"{measure}Change"}, inplace = True)

    return latest_chg

def process_unemployment(home_dir):
    # get latest file
    directory = f"{home_dir}/data/unemployment"
    path = get_latest_file(directory)

    # Read & filter data
    df = pd.read_csv(path, low_memory = False)
    df = df[df["SUBJECT"] == "TOT"]

    # Split into quarterly and yearly
    q_df = df[df["TIME"].str.contains("-Q[1-4]")]
    y_df = df[df["TIME"].str.contains("^[0-9]{4}$")]

    q_chg = pct_chg_and_merge(q_df, "QuarterlyUnemploymentRate")
    y_chg = pct_chg_and_merge(y_df, "YearlyUnemploymentRate")

    # combined
    chg = pd.concat([q_chg, y_chg], axis = 1)

    # convert iso code to country name
    country_ref = get_country_iso_code()
    combined = chg.merge(country_ref, left_index = True, right_index = True, how = "inner").fillna(0.)
    combined.set_index("Country", inplace = True)

    # assign rank
    for column in combined.columns:
        combined[f"{column}Rank"] = assign_rank(combined[column], "ascending")

    # save
    combined.to_csv(f"{home_dir}/insights/unemployment/latest.csv", header = True, index = True)

# if __name__ == "__main__":
#     process_unemployment()


