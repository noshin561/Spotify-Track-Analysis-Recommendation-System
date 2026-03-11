import pandas as pd

def load_and_clean_data():

    df = pd.read_csv("track_data_final.csv")

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Remove null values
    df.dropna(inplace=True)

    # Select important columns
    df = df[['track_name', 'track_popularity', 'explicit']]

    return df