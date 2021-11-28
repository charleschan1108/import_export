"""
idx3() calculates and returns trade dependency of a country
"""
def tradeDependency(country, df_gdp, df_import, df_export):

    country = country.title()  #change first char to capital
    gdpValue = float(
        df_gdp.loc[df_gdp['country'] == country]['2020'].str.replace(',',''))
    importValue = float(
        df_import.loc[df_import['Country'] == country]['Imports (Billion $)'].str.replace(',',''))
    exportValue = float(
        df_export.loc[df_export['Country'] == country]['Exports (Billion $)'].str.replace(',',''))
    return ((importValue + exportValue)/gdpValue)