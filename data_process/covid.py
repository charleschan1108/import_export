import pandas as pd
import numpy as np

from datetime import datetime

from .utils import assign_rank

qmap = {
    "01": "Q1",
    "02": "Q1",
    "03": "Q1",
    "04": "Q2",
    "05": "Q2",
    "06": "Q2",
    "07": "Q3",
    "08": "Q3",
    "09": "Q3",
    "10": "Q4",
    "11": "Q4",
    "12": "Q4"
}

def process_covid(home_dir):
    stat_columns = ["total_cases", 
                    "total_deaths", 
                    # "total_tests", 
                    "people_fully_vaccinated", 
                    "population"
                    ]

    # Read & Filter data
    data = pd.read_csv(f"{home_dir}/data/covid/owid-covid-data.csv")
    data = data.loc[:, ["date", "location"] + stat_columns]
    # print(data)

    # pivot data
    pivot = data.pivot(index = "date", columns = ["location"], values = stat_columns).ffill()

    # convert to quarter
    data["time"] = data["date"].apply(lambda x: x[:4] + f"-{qmap[x[5:7]]}")
    q_data = data.groupby("time", as_index = False)["date"].max()
    q_pivot = q_data.merge(pivot.reset_index().drop(columns = ["population"]), left_on = "date", right_on = "date", how = "inner").set_index("time")
    q_pivot.drop(columns = ["date"], inplace = True)
    
    # get rate of change quarterly & yearly
    chg = q_pivot.pct_change().ffill()
    q_chg = chg.iloc[-1]
    y_chg = chg.iloc[-1] / chg.iloc[-4] - 1
    
    # combine
    combine = pd.concat([q_chg, y_chg], axis = 1).reset_index()
    combine["value"] = combine["index"].apply(lambda x: x[0])
    combine["Country"] = combine["index"].apply(lambda x: x[1])
    combine.drop(columns = ["index"], inplace = True)
    combine.rename(columns = {q_chg.name: "QuarterlyChange", 0: "YearlyChange"}, inplace = True)
    combine = combine.pivot(index = "Country", columns = "value", values = ["QuarterlyChange", "YearlyChange"])
    
    # add vaccine / population
    # combine["fully_vaccinated_rate"] = pivot.iloc[-1]["people_fully_vaccinated"] / pivot.iloc[-1]["population"]
    q_combine = combine["QuarterlyChange"]
    q_combine.rename(columns = {column: "QuarterlyChange_" + column for column in q_combine.columns}, inplace = True)
    y_combine = combine["YearlyChange"]
    y_combine.rename(columns = {column: "YearlyChange_" + column for column in y_combine.columns}, inplace = True)
    vac_rate = pivot.iloc[-1]["people_fully_vaccinated"] / pivot.iloc[-1]["population"]
    vac_rate.rename("vaccinated_rate", inplace = True)
    
    combine = q_combine.merge(y_combine, left_index = True, right_index = True, how = "inner")
    combine = combine.merge(vac_rate, left_index = True, right_index = True, how = "inner")
    combine.fillna(0., inplace = True)

    # assign rank
    for column in combine.columns:
        if column.endswith("vaccinated") | (column == "vaccinated_rate"):
            combine[f"{column}Rank"] = assign_rank(combine[column], "descending")
        else:
            combine[f"{column}Rank"] = assign_rank(combine[column], "ascending")

    # Save
    combine.to_csv(f"{home_dir}/insights/covid/latest.csv", header = True, index = True)

# if __name__ == "__main__":
    