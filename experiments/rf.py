import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_absolute_error
import pandas as pd
import csv

"""
Random Forest for solar prediction
"""

# path to the csv file to use
# TODO: replace this with a data.Dataset object
# DATASET = "/media/zach/Elements/SolarData/24_hr_results/all_attributes/griffin.csv"
DATASET = "/media/zach/PNY_32GB/SolarData/24_hr_results/all_attributes_and_window/data-griffin.csv"
# DATASET = "/media/zach/Elements/SolarData/24_hr_results/multi_cell/griffin.csv"
# DATASET = "/media/zach/Elements/SolarData/1_hr_results/multi_cell/data.csv"
HAS_HEADER = True  # does the csv have a header with column names?

# params for rf regressor
params = {
    "n_estimators": 100,
    "criterion": "mse",
    "max_features": None,
    "max_depth": 15,
    "min_samples_split": 2,
    "bootstrap": True,
    "random_state": 1
}

# read dataset
df = pd.read_csv(DATASET, sep=',')
X = df[df.columns.tolist()[:-1]].values
y = df[df.columns.tolist()[-1]].values

regressor = RandomForestRegressor(**params)
# regressor.fit(X, y)
scores = cross_val_score(regressor, X, y, cv=10, scoring='neg_mean_absolute_error', n_jobs=-1)
print("Random Forest")
print(DATASET)
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
