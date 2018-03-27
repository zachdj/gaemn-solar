"""
Random Forest for solar prediction
"""

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from texttable import Texttable
import os

from solarrad import Dataset

# site ids for the five sites in Sam's paper
sites = {
    "griffin": 115,
    "jonesboro": 380,
    "attapulgus": 190,
    "blairsville": 150,
    "brunswick": 420
}

# params for rf regressor
rf_params = {
    "n_estimators": 100,
    "criterion": "mse",
    "max_features": None,
    "max_depth": 20,
    "min_samples_split": 2,
    "bootstrap": True,
    "random_state": 123
}


def do_experiment(hour, site, gaemn=False, window=False, nam_cell=False, nam_grid=False):
    dataset = Dataset.generate_from_query(target_hour=hour, site_id=site, gaemn=gaemn, window=window, nam_cell=nam_cell,
                                          nam_grid=nam_grid)
    X_train, X_test, y_train, y_test = train_test_split(dataset.data, dataset.labels, test_size=0.20, random_state=123)
    regressor = RandomForestRegressor(**rf_params)
    regressor.fit(X_train, y_train)
    predictions = regressor.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    return mae


# iterate over all sites
for site_name, site_id in sites.items():
    print("Working on site %s" % site_name)
    # construct TextTable for writing out results
    table = Texttable()
    table.set_cols_align(["c", "c", "c", "c", "c", "c"])
    table.header(["Hour", "gaemn only", "gaemn+window", "gaemn + window + single-cell", "gaemn + window + multicell", "% decrease"])

    # do an experiment for each hour and each dataset
    for hour in list(range(1, 37)):
        print("Hour %d" % hour)
        all_attr_mae = do_experiment(hour, site_id, gaemn=True)
        window_mae = do_experiment(hour, site_id, gaemn=True, window=True)
        singlecell_mae = do_experiment(hour, site_id, gaemn=True, window=True, nam_cell=True)
        multicell_mae = do_experiment(hour, site_id, gaemn=True, window=True, nam_cell=True, nam_grid=True)
        pct_improvement = (window_mae - multicell_mae) * 100 / window_mae
        table.add_row([hour, all_attr_mae, window_mae, singlecell_mae, multicell_mae, pct_improvement])

    # output the table to a file:
    outpath = os.path.join("../results", site_name+".txt")
    with open(outpath, 'w') as outfile:
        print(site_name.capitalize(), file=outfile)
        print(table.draw(), file=outfile)

print("Done!")
