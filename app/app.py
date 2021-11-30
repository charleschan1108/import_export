import pandas as pd
import numpy as np

from datetime import datetime

pd.set_option('display.max_rows', None)

from .utils import assign_rank
from .utils import get_trade_partner
# from config import weighting

weighting = {
    "vaccinated_rateRank": 0.2,
    "casesRank": 0.2,
    "deathsRank": 0.2,
    "GdpChangeRank": 0.1,
    "InflationRank": 0.1,
    "IMPRank": 0.3,
    "EXPRank": 0.3,
    "NTRADERank": 0.3,
    "UnemploymentRateChangeRank": 0.1,
    "GdpTradeCompRank": 0.1
}

# rescale weighting
total = sum(weighting.values())
for key in weighting.keys():
    weighting[key] = weighting[key] / total

insights_dir = [
    "covid",
    "gdp",
    "inflation",
    "trade",
    "unemployment",
]

def compute_overall_rank(df, weighting = None):
    if weighting is not None:
        dfs = []
        for column in df.columns:
            for key in weighting.keys():
                if column.endswith(key):
                    dfs.append(df[column] * weighting[key])
    
        res =  sum(dfs)
    else:
        res = df.mean(axis = 1)

    return assign_rank(res, "ascending")

def display_with_country(df, perspective_country, term, topn = 10):
    trade_parter = get_trade_partner()
    pc_df = trade_parter[trade_parter["Country"] == perspective_country]

    if pc_df.shape[0] < 1:
        print(f"Country {perspective_country} is not found in database.")
        return

    # top imported & exported countries
    top_imported = pc_df["Top import partners"].apply(eval).tolist().pop()
    top_exported = pc_df["Top export partners"].apply(eval).tolist().pop()

    # export
    exp_df = df[df.index.isin(top_exported)]
    imp_df = df[df.index.isin(top_imported)]

    # compute overall rank
    run_time = datetime.now().isoformat()

    print(f"For {perspective_country}, the best export partners in {term}:")
    exp_df["Overall Rank"] = compute_overall_rank(exp_df)
    exp_df = exp_df.sort_values("Overall Rank", ascending = True)
    print(exp_df.head(topn))
    print(f"Check {run_time}_export.csv for more details.")
    exp_df.to_csv(f"{run_time}_export_{term}.csv", header = True, index = True)

    print(f"For {perspective_country}, the best import partners in {term}:")
    imp_df["Overall Rank"] = compute_overall_rank(imp_df)
    imp_df = imp_df.sort_values("Overall Rank", ascending = True)
    print(imp_df.head(topn))
    print(f"Check {run_time}_import.csv for more details.")
    imp_df.to_csv(f"{run_time}_import_{term}.csv", header = True, index = True)

    # TODO: add plot

def display_without_country(df, term, topn = 10):
    run_time = datetime.now().isoformat()

    # compute overall rank
    print(f"In general, the best trade partners in {term} are")
    df["Overall Rank"] = compute_overall_rank(df)
    df = df.sort_values("Overall Rank", ascending = True)
    print(df.head(topn))
    print(f"Check {run_time}_general_{term}.csv for more details.\n\n")

    df.to_csv(f"{run_time}_general_{term}.csv", header = True, index = True)

    # TO DO: add plot


def app(home_dir, perspective_country = None, weighting = None, topn = 10):
    # load insights
    dfs = [pd.read_csv(f"{home_dir}/insights/{directory}/latest.csv", index_col = 0) for directory in insights_dir]
    df = pd.concat(dfs, axis = 1)
    
    # get QGDP is not null countries
    df = df[~df["QGDP"].isnull()]

    # Cross logic
    df["GdpTradeComp"] = (df["EXP"] - df["IMP"])/df["QGDP"]
    df["GdpTradeCompRank"] = assign_rank(df["GdpTradeComp"], "descending")
    
    # keep only columns with name ends with Rank
    df = df[[column for column in df if column.endswith("Rank")]]

    # Split into short/long term df
    sdf = df[[column for column in df.columns if "yearly" not in column.lower()]]
    ldf = df[[column for column in df.columns if "quarterly" not in column.lower()]]
    
    if perspective_country is not None:
        display_with_country(sdf, perspective_country, "short term (quarterly data)", topn = topn)
        display_with_country(ldf, perspective_country, "long term (yearly data)", topn = topn)
    else:
        display_without_country(sdf, "short term (quarterly data)", topn = topn)
        display_without_country(ldf, "long term (yearly data)", topn = topn)
        
        
if __name__ == "__main__":
    # app(perspective_country = "China", weighting = weighting)
    app(weighting = weighting)