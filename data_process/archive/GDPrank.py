import pandas as pd

file = pd.read_csv('gdp.csv')
predictValue = pd.DataFrame(columns=['Country', 'Time', 'GDP'])
newFile = pd.DataFrame(file.loc[(file['MEASURE'] == 'IDX') &
                                (file['SUBJECT'] == 'VOLIDX')])

i = 0
index = 1
location = pd.Series(0, index=pd.RangeIndex(0, 150))
f_location = newFile['LOCATION']
location[0] = f_location.iloc[0]
locationIndex = location[0]
for num in f_location:
    if num == locationIndex:
        i += 1
        continue
    else:
        location[index] = num
        locationIndex = num
        i += 1
        index += 1

location = location[location != 0]
for country in location:
    f = pd.DataFrame(newFile.loc[(newFile['LOCATION'] == country)])
    f.index = f['TIME'].values
    if f.iloc[-1]['TIME'] != '2021-Q3':
        continue
    f_new = pd.DataFrame(f.loc['2018-Q1':'2021-Q3'])
    f_new = f_new[['LOCATION', 'Value']]
    f_Value = f_new['Value']
    rate = pd.Series(index=pd.RangeIndex(0, 15))
    i = 0
    for index in f_Value:
        if i <= 13:
            former = float(f_Value[i])
            latter = float(f_Value[i + 1])
            rate[i] = float((latter - former) / former)
            i += 1
    newValue = float(f_Value['2021-Q3']) * (1 + rate[13])
    f_new.loc['2021-Q4'] = [country, newValue]
    predictValue.loc[country] = [country, '2021-Q4', newValue]

rankGDP = predictValue.sort_values('GDP', ascending=False)
rankGDP.index = range(1, len(predictValue.index)+1)
numRank = input("The total country for GDP rank is "+str(len(predictValue.index))+". Please enter the number you want to display for TOPN: ")
print(rankGDP.iloc[0:int(numRank)])