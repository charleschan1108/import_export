# import_export

This package is designed to support companies to make informed decision pertaining to their cross boarder trading activities. 

## Set up
It is better to create a virtual environment for this project since it will not affect your existing python environment.

### Step 0: Download ChromeDriver
Go to https://chromedriver.chromium.org/ and download the suitable version chromedriver for your computer. And place it in the home directory of this repo.

### Step 1: Clone the repository and get the source code ready in your computer
```
# clone repo
git clone https://github.com/charleschan1108/import_export.git

# change directory
cd import_export
```

### Step 2: Create a virtual environment named env
```
python -m venv env
```

### Step 3: Activate the env virtual environment
```
source env/bin/activate
```

### Step 4: Install packages
```
pip install selenium
pip install pandas
pip install numpy
pip install beautifulsoup4
pip install requests
```

## Manuals

Currently, this package has two applications:
1. For a specified country, which country is the best partners for export/import during and after this pandemic?
2. In general, which country is the best partners for trade of goods and services during and after this pandemic?

## Application 1: For specified country
```
# With data being refreshed
# it takes around 3 mins to refresh the data
python main.py --refresh 1 --country China

# Without data being refreshed
python main.py --refresh 0 --country China
```

Sample output:
```
YearlyChange_people_fully_vaccinatedRank  YearlyChange_total_casesRank  YearlyChange_total_deathsRank  ...  YearlyUnemploymentRateRank  GdpTradeCompRank  Overall Rank
Country                                                                                                               ...                                                            
Japan                                              46.0                          20.0                           32.0  ...                         2.0                43             1
South Korea                                       122.0                         167.0                          152.0  ...                         6.0                18             2
United States                                     227.0                         116.0                          112.0  ...                        27.0                47             3

YearlyChange_people_fully_vaccinatedRank  YearlyChange_total_casesRank  YearlyChange_total_deathsRank  ...  YearlyUnemploymentRateRank  GdpTradeCompRank  Overall Rank
Country                                                                                                               ...                                                            
Japan                                              46.0                          20.0                           32.0  ...                         2.0                43             1
South Korea                                       122.0                         167.0                          152.0  ...                         6.0                18             2
United States                                     227.0                         116.0                          112.0  ...                        27.0                47             3
```

## Application 2: For any country

```
python main.py --refresh 0
```

Sample output:
```
QuarterlyChange_people_fully_vaccinatedRank  QuarterlyChange_total_casesRank  QuarterlyChange_total_deathsRank  ...  QuarterlyUnemploymentRateRank  GdpTradeCompRank  Overall Rank
Country                                                                                                                         ...                                                               
Czech Republic                                          NaN                              NaN                               NaN  ...                            4.0                19             1
Japan                                                 113.0                             57.0                             106.0  ...                            5.0                43             2
Saudi Arabia                                          133.0                             45.0                              69.0  ...                            NaN                 5             3
Indonesia                                              48.0                             54.0                              68.0  ...                            NaN                14             4
Colombia                                               85.0                             71.0                              72.0  ...                           35.0                36             5
South Korea                                            71.0                            209.0                             214.0  ...                            6.0                18             6
Chile                                                 148.0                            110.0                              87.0  ...                           32.0                20             7
Sweden                                                179.0                            100.0                              79.0  ...                           33.0                21             8
Italy                                                 176.0                            116.0                              84.0  ...                           34.0                11             9
Switzerland                                           153.0                            173.0                             100.0  ...                            2.0                 9            10

YearlyChange_people_fully_vaccinatedRank  YearlyChange_total_casesRank  YearlyChange_total_deathsRank  ...  YearlyUnemploymentRateRank  GdpTradeCompRank  Overall Rank
Country                                                                                                                ...                                                            
Japan                                               46.0                          20.0                           32.0  ...                         2.0                43             1
Indonesia                                           53.0                          15.0                           22.0  ...                         NaN                14             2
Italy                                               48.0                          82.0                           50.0  ...                        31.0                11             3
France                                              17.0                          84.0                           49.0  ...                        26.0                44             4
Czech Republic                                       NaN                           NaN                            NaN  ...                         1.0                19             5
Sweden                                             143.0                          51.0                           38.0  ...                        29.0                21             6
Chile                                              103.0                          81.0                           55.0  ...                        33.0                20             7
Saudi Arabia                                       135.0                          64.0                          108.0  ...                         NaN                 5             8
Portugal                                           221.0                          67.0                           26.0  ...                        24.0                37             9
Spain                                              120.0                          53.0                           44.0  ...                        35.0                38            10

```

## Additional functions

### Weighting

The above example assume user put equal weight on factors:
* number of covid case
* number of death by covid
* vaccinated rate
* GDP growth
* Inflation
* Export/Import/Net Trade values
* Net trade / GDP
* Unemployment rate

Users can specify their weighting in config.py:
```
# config.py

weighing = {
    "vaccinated_rateRank": 0.2,
    "casesRank": 0.2,
    "deathsRank": 0.2,
    "GdpChangeRank": 0.1,
    "InflationRank": 0.1,
    "IMPRank": 0.3,
    "EXPRank": 0.3,
    "NTRADERank": 0.3,
    "UnemploymentRateChangeRank": 0.1
}
```

The module will normalize the weighting (i.e. such that the weightings sum to one) and plugged into the calculation of overall rank in the final output.

To enable weighting, the command becomes:
```
python main.py --refresh 0 --equal_weight 0
```

### TopN

Users can specify the argument topn to control the number of output to display in console.

Example snippet:
```
python main.py --refresh 0 --equal_weight 0 --topn 10
```


### Others

For more details, you can use the following command:
```
python main.py -h
```

## Package Logic

This package consists of 3 parts:
1. Data ingestion to crawl raw data
2. Data process to massage data
3. Application

### Data ingestion
All the crawlers are stored in the data_ingestion module. They will crawl the designated data from the specified websites and stored into the data directory.

### Data process
All the data processors are stored in the data_process module. They will process the raw data according to the logic specified and save the output at the insights directory.

### Application
Provide users with API to interact with the insights uncovered in the previous part.