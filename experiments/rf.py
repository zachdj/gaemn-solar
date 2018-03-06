"""
Random Forest for solar prediction
"""

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from texttable import Texttable

from solarrad import Dataset

# generate a dataset
dataset = Dataset.generate_from_query(target_hour=24, site_id=115, gaemn=True, window=True, nam_cell=True, nam_grid=False)

# params for rf regressor
params = {
    "n_estimators": 20,
    "criterion": "mse",
    "max_features": None,
    "max_depth": 20,
    "min_samples_split": 2,
    "bootstrap": True,
    "random_state": 123
}

X_train, X_test, y_train, y_test = train_test_split(dataset.data, dataset.labels, test_size=0.20, random_state=123)

regressor = RandomForestRegressor(**params)
regressor.fit(X_train, y_train)

predictions = regressor.predict(X_test)
correlation = r2_score(y_test, predictions)
mse = mean_squared_error(y_test, predictions)
mae = mean_absolute_error(y_test, predictions)

print("RF on %s" % dataset.name)
print("Corr: %0.4f \n MSE: %0.4f \n MAE: %0.4f" % (correlation, mse, mae))
