# A simple function to transform names of some countries
# Now it only works with some countries mainly use abbreviation
# Please let me know if there are other countries using abbreviation in our data source,
# or just edit the code and don't forget to upload it to Canvas ——Yigang
def countryNameHandle(country_name):
    country_name = country_name.strip()
    if(country_name.startwith("The") or country_name.startwith("the")):
        country_name = country_name[3:]
    country_name = country_name.lower()
    if(country_name=="usa" or country_name=="us" or country_name=="unitedstates"):
        country_name = "america"
    elif(country_name=="britain" or country_name=="england"):
        country_name = "unitedkingdom"
    return country_name