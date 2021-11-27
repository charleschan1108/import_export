import pandas as pd

from utils import get_latest_file

if __name__ == "__main__":
    directory = "../data/inflation_mom"
    path = get_latest_file(directory)

    print(path)