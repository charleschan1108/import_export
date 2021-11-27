import os

def get_latest_file(directory):
    paths = os.listdir(directory)
    return max(paths)