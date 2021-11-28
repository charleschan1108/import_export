import pandas as pd
import numpy as np

from .utils import assign_rank
from .utils import get_latest_file
from .utils import get_country_iso_code

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