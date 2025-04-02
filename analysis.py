import pandas as pd

def analyze_data(df):
    stats = df.describe().to_dict()
    return stats
