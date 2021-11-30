def idx1():
    #data preparation
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from webdriver_manager.chrome import ChromeDriverManager
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
    from pandas.core.frame import DataFrame
    html = "https://www.arcgis.com/apps/dashboards/bda7594740fd40299423467b48e9ecf6"
    from time import sleep,time
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get(html)
    sleep(60)
    classlst = browser.find_elements(By.CLASS_NAME,"external-html")
    classlen = len(classlst)
    half = int(classlen/2)
    newelef = []
    exp = classlst[0:half]
    for j in exp:
        for i in j.find_elements(By.TAG_NAME,"span"):
            newelef.append(i.text)
    countryname = []
    for i in classlst:
        countryname.append(i.find_element(By.TAG_NAME,"span").text)
    countrylist = [i for i in countryname if i!=""]
    numlst = []
    for i in newelef:
        if i.find("|")!=-1:
            if i.find("Totals:")!=-1:
                numlst.append(i.strip("Totals: "))
            else:
                numlst.append(i)
    temp = [i.split(" | ")for i in numlst]
    list_28 = []
    list_Total = []
    idx = 0
    for i in temp:
        if (idx%2) == 0:
            list_28.append(i)
            idx += 1
        else:
            list_Total.append(i)
            idx -= 1
    cases_28=[]
    death_28 = []
    for i in list_28:
        cases_28.append(i[0])
        death_28.append(i[1])
    cases_Total=[]
    death_Total = []
    for i in list_Total:
        cases_Total.append(i[0])
        death_Total.append(i[1])
    table = {"Country":countrylist,
            "Cases(28-Day)":cases_28,
            "Death(28-Day)":death_28,
            "Cases(Total)":cases_Total,
            "Death(Total)":death_Total,
            }
    data = DataFrame(table)

    data.iloc[0]["Country"]="United States"

    import pandas as pd
    import numpy as np

    # vaccine = pd.read_excel("/Users/ruipan/Desktop/idx1/Vaccine.xlsx",sheet_name = "owid-covid-data")

    # data2 = vaccine[['location','date','hosp_patients_per_million', 'weekly_hosp_admissions_per_million','people_fully_vaccinated_per_hundred',
    #        'population','population_density','median_age','hospital_beds_per_thousand']]

    #process type

    def changetoint(series):
        lst = []
        for i in series:
            lst.append(int(i.replace(",","")))
        series = np.array(lst)
        return series

    data["Cases(28-Day)"] = changetoint(data["Cases(28-Day)"])
    data["Cases(Total)"] = changetoint(data["Cases(Total)"])
    data["Death(28-Day)"] = changetoint(data["Death(28-Day)"])
    data["Death(Total)"] = changetoint(data["Death(Total)"])

    #indicator

    data["case_rate_increase_month"] = data["Cases(28-Day)"]/(data["Cases(Total)"]-data["Cases(28-Day)"])
    data["death_rate_increase_month"]=data["Death(28-Day)"]/(data["Death(Total)"]-data["Death(28-Day)"])

    data.to_csv("../data/covid.csv", header = True, index = True)

    # data2.loc[:,"increase_rate_week"] =data2["weekly_hosp_admissions_per_million"]/(data2["hosp_patients_per_million"]-data2["weekly_hosp_admissions_per_million"])

    # data2.loc[:,"admission_rate"] = data2["hosp_patients_per_million"]/(data2["population"]/1000000)

    # #28days

    # from datetime import date,timedelta
    # today = date.today()

    # d = today - timedelta(days=28)

    # data2.loc[:,"date"]=[i.date() for i in data2["date"]]

    # data2_28=data2.loc[data2["date"]>d,:]

    # pos_factor =data2_28[["location","people_fully_vaccinated_per_hundred","hospital_beds_per_thousand","admission_rate","population"]].groupby(by ="location").agg("mean")

    # neg_factor= data[["Country","case_rate_increase_month","death_rate_increase_month","Cases(28-Day)"]]

    # factor28=pd.merge(neg_factor,pos_factor,left_on = 'Country', right_on = 'location',how = "left")

    # factor28["Infection_rate"]=factor28["Cases(28-Day)"]/factor28["population"]

    # #cumulative

    # pos_factor2 =data2[["location","people_fully_vaccinated_per_hundred","hospital_beds_per_thousand","admission_rate","population"]].groupby(by ="location").agg("mean")

    # neg_factor2= data[["Country","Cases(Total)"]]

    # factortotal=pd.merge(neg_factor2,pos_factor2,left_on = 'Country', right_on = 'location',how = "left")

    # factortotal["Infection_rate"]=factortotal["Cases(Total)"]/factortotal["population"]

    # #display 2 tables(28-day and total)

    # idx_28 = factor28["Infection_rate"]/(factor28["people_fully_vaccinated_per_hundred"]*factor28["hospital_beds_per_thousand"])

    # idx_total = factortotal["Infection_rate"]/(factortotal["people_fully_vaccinated_per_hundred"]*factortotal["hospital_beds_per_thousand"])

    # return idx_28,idx_total,factor28,factortotal