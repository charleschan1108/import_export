"""
app/app.py
Author: 
    Charles Chan, Hsueh-i Lu, Rui Pan, Yaheng Wang, Yigang Zhou, Jiaqi Song

Description: 
    This script here is to store all functions related to the applications of our product.

    Application:
        Compute the overall rank according customised or equal weighting
        Some visualization for the top recommended trading countries

Import by:
    main.py
"""

import pandas as pd
import numpy as np

from datetime import datetime

pd.set_option('display.max_rows', None)

from .utils import assign_rank
from .utils import get_trade_partner
from .utils import get_latest_file
from .utils import get_country_iso_code
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

"""
Function:
    plot
Purpose:
    For the top 10 trading partners countries, visualize the pandemic and the trading situation
Inputs:
    :param: df -- retrieved raw data from data directory
    :param: column -- which column to plot. column chosen to be the value of the pivot table
    :param: datecol -- column chosen to be the index of the pivot table
    :param: loccol -- series chosen to be the columns of the pivot table
    :param: title (nullable) -- Title for the plot
    :param: savepath (nullable) -- save path for the plot
    :param: ylabel (nullable) -- ylabel for the plot

Output:
    Save the plot to the savepath
"""
def plot(df, column, datecol = "date", loccol = "location", title = None, savepath = None, ylabel = None):
    plot_df = df.pivot(index = datecol, columns = loccol, values = column)
    f = plot_df.plot.line()
    f.figure.set_size_inches(12, 8)
    
    if bool(title):
        f.set_title(title)
    
    if bool(ylabel):
        f.set_ylabel(ylabel)
    
    if savepath is not None:
        f.figure.savefig(savepath)

"""
Function:
    plot_raw_data
Purpose:
    Preprocess the raw data first before passing into the plot function for visualization.
Inputs:
    :params: home_dir -- the home directory for the function to find the right directory to save data
    :params: countries -- Which countries data to be plot (Top 10 from the analysis measured by the overall rank)
Output:
    Save the plot to the savepath
"""
def plot_raw_data(home_dir, countries):
    # Load covid data
    covid = pd.read_csv(f"{home_dir}/data/covid/owid-covid-data.csv")
    covid = covid[covid["location"].isin(countries)]
    covid["vaccinated_rate"] = covid["people_fully_vaccinated"] / covid["population"]

    # Load trade data: export, import and netrade
    path = get_latest_file(f"{home_dir}/data/trade")
    country_ref = get_country_iso_code()
    country_ref = country_ref[country_ref.isin(countries)]

    trade = pd.read_csv(path)
    trade = trade[trade["TIME"].str.contains("20[12][0-9]")]
    exp = trade.loc[trade["LOCATION"].isin(country_ref.index) 
                    & (trade["SUBJECT"] == "EXP")
                    & (trade["MEASURE"] == "BLN_USD")
                    & (trade["FREQUENCY"] == "M")]
    imp = trade.loc[trade["LOCATION"].isin(country_ref.index) 
                    & (trade["SUBJECT"] == "IMP")
                    & (trade["MEASURE"] == "BLN_USD")
                    & (trade["FREQUENCY"] == "M")]
    NTRADE = trade.loc[trade["LOCATION"].isin(country_ref.index) 
                    & (trade["SUBJECT"] == "NTRADE")
                    & (trade["MEASURE"] == "BLN_USD")
                    & (trade["FREQUENCY"] == "M")]

    # plot covid
    plot(covid, "vaccinated_rate", title = "Top 10 Countries Vaccinated Rate", ylabel = "Vaccinated Rate", savepath = f"{home_dir}/Top10_vac_rate.png")
    plot(covid, "hosp_patients_per_million", title = "Top 10 Countries Hospitalized Patients per million", ylabel = "Hospitalized Patients per million",
    savepath = f"{home_dir}/Top10_HospPerMillion.png")

    # plot trade
    plot(exp, "Value", datecol = "TIME", loccol = "LOCATION", title = "Top 10 Countries Value of Export Goods", ylabel = "$USD (Billion)",
    savepath = f"{home_dir}/Top10_export.png")
    plot(imp, "Value", datecol = "TIME", loccol = "LOCATION", title = "Top 10 Countries Value of IMPORT Goods", ylabel = "$USD (Billion)",
        savepath = f"{home_dir}/Top10_import.png")
    plot(NTRADE, "Value", datecol = "TIME", loccol = "LOCATION", title = "Top 10 Countries Value of NET TRADE Goods", ylabel = "$USD (Billion)",
        savepath = f"{home_dir}/Top10_ntrade.png")

"""
Function:
    compute_overall_rank
Purpose:
    Compute the overall rank according to other series using weighted average or equal weight average of the rank of
    other series.
Inputs:
    :params: df -- filtered data frame of other ranked series
    :params: weighting (nullable) -- None for computing equal weighted average of rank or input a dictionary of weighting
Output:
    df with overall rank assigned.
"""
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

"""
Function:
    display_with_country
Purpose:
    Display the final results to the console for a specified country (perspective_country)
Inputs:
    :params: df -- filtered data frame of other ranked series
    :params: perspective_country -- country of interest
    :params: term -- short or long term. Only affect the logging
    :params: home_dir -- the home directory for the function to find the right directory to save data
    :params: topn -- how many results to display in the final output.
Output:
    Results displayed in the console.
"""
def display_with_country(df, perspective_country, term, home_dir, topn = 10):
    trade_partner = get_trade_partner()
    pc_df = trade_partner[trade_partner["Country"] == perspective_country]

    if pc_df.shape[0] < 1:
        print(f"Country {perspective_country} is not found in database.")
        return

    # top imported & exported countries
    top_imported = pc_df["Top import partners"].apply(eval).tolist().pop()
    top_exported = pc_df["Top export partners"].apply(eval).tolist().pop()

    # export
    exp_df = df[df.index.isin(top_exported)]
    imp_df = df[df.index.isin(top_imported)]

    # set index of trade_partner as Country
    trade_partner.set_index("Country", inplace = True)

    # compute overall rank
    run_time = datetime.now().isoformat()

    print(f"For {perspective_country}, the best export partners in {term}:")
    exp_df["Overall Rank"] = compute_overall_rank(exp_df)
    exp_df = trade_partner[["Top exported products"]].merge(exp_df.sort_values("Overall Rank", ascending = True),
                left_index = True, right_index = True, how = "right")
    print(exp_df.head(topn))
    print(f"Check {run_time}_export.csv for more details.")
    exp_df.to_csv(f"{run_time}_export_{term}.csv", header = True, index = True)

    print(f"For {perspective_country}, the best import partners in {term}:")
    imp_df["Overall Rank"] = compute_overall_rank(imp_df)
    imp_df = trade_partner[["Top imported products"]].merge(imp_df.sort_values("Overall Rank", ascending = True),
                left_index = True, right_index = True, how = "right")
    print(imp_df.head(topn))
    print(f"Check {run_time}_import.csv for more details.")
    imp_df.to_csv(f"{run_time}_import_{term}.csv", header = True, index = True)

    # plot results
    countries = list(set(exp_df.index[:5].tolist() + imp_df.index[:5].tolist()))
    plot_raw_data(home_dir, countries)

"""
Function:
    display_with_country
Purpose:
    Display the final results to the console without specifying a country
Inputs:
    :params: df -- filtered data frame of other ranked series
    :params: term -- short or long term. Only affect the logging
    :params: home_dir -- the home directory for the function to find the right directory to save data
    :params: topn -- how many results to display in the final output.
Output:
    Results displayed in the console.
"""
def display_without_country(df, term, home_dir, topn = 10):
    trade_parter = get_trade_partner().set_index("Country")[["Top exported products", 'Top imported products']]

    run_time = datetime.now().isoformat()

    # compute overall rank
    print(f"In general, the best trade partners in {term} are")
    df["Overall Rank"] = compute_overall_rank(df)
    df = trade_parter.merge(df.sort_values("Overall Rank", ascending = True),
            left_index = True, right_index = True, how = "right")
    print(df.head(topn))
    print(f"Check {run_time}_general_{term}.csv for more details.\n\n")

    df.to_csv(f"{run_time}_general_{term}.csv", header = True, index = True)

    # plot results
    plot_raw_data(home_dir, df.index[:10])

"""
Function:
    app
Purpose:
    A function to wrap all the logics of the application. For details, please refer to the README.md.
Inputs:
    :params: home_dir -- the home directory for the function to find the right directory to save data
    :params: perspective_country (nullable) -- The country to find the best trading partners countries for. 
                                                Leave it null to find the best partners in general.
    :params: weighting (nullable) -- None for computing equal weighted average of rank or input a dictionary of weighting
    :params: topn -- how many results to display in the final output.
Output:
    Results displayed in the console.
"""
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
        display_with_country(sdf, perspective_country, "short term (quarterly data)", home_dir=home_dir, topn = topn)
        display_with_country(ldf, perspective_country, "long term (yearly data)", home_dir=home_dir, topn = topn)
    else:
        display_without_country(sdf, "short term (quarterly data)", home_dir=home_dir, topn = topn)
        display_without_country(ldf, "long term (yearly data)", home_dir=home_dir, topn = topn)
        
        
if __name__ == "__main__":
    # app(perspective_country = "China", weighting = weighting)
    app(weighting = weighting)