import pandas as pd

def readCsv(path):
    df = pd.read_csv(path)
    return df
