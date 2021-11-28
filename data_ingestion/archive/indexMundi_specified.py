from bs4 import BeautifulSoup as bs
import requests as req
import pandas as pd


# use t and v to get data in certain sheet
# t means Top N country for certain data. t=0 means get all countries' data, recommended.
# v means kind of data. v=89 for Imports, v=85 for Exports
# Go https://www.indexmundi.com/g/r.aspx?t=0&v=85&l=en, choose which kind of data you want and submit,
# then you can see the value of t and v in URL
# the function return a DataFrame. 1st column is rank, 2nd is name of country, 3rd is data
def indexMundiGetDataFrame(t, v):
    url_path = "https://www.indexmundi.com/g/r.aspx?t=" + str(t) + "&v=" + str(v)
    r = req.get(url_path)
    demo = r.text  # server respond
    soup = bs(demo, "html.parser")
    data_table = soup.find('table', {'border': '0'})
    table_row = data_table.children  # get all the tr
    heads = []
    contents = []
    counts = 0
    for a in table_row:
        content = []
        for b in a.children:  # b is th or tb
            text = b.get_text()
            if (counts < 3):
                heads.append(text)
            else:
                if (len(content) == 3):
                    contents.append(content)  # only need 3 column, the 4th is empty
                if (text != ''):
                    content.append(text)
            counts += 1

    df = pd.DataFrame(columns=heads)  # use DataFrame to quickly build data

    for x in contents:
        df = df.append({heads[0]: x[0],
                        heads[1]: x[1],
                        heads[2]: x[2]
                        }, ignore_index=True)
    return df
