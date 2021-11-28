weighting = {
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

# rescale weighing
total = sum(weighting.values())
for key in weighting.keys():
    weighting[key] = weighting[key] / total