import os

def get_latest_file(directory):
    paths = os.listdir(directory)
    return os.path.join(directory, max(paths))