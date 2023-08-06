import pandas as pd

assets = pd.read_csv("ames_train_cleaned.csv")


def is_new(col):
    return col > 1970


assets["is_new"] = is_new(assets["Year_Built"])
y = assets["is_new"]
