""" Train a RF model using a variety of inputs for every target hour from 1-36
"""

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from texttable import Texttable
import os

from solardata.Dataset import Dataset
from solardata.query import Query
import solardata.sites as sites

# output directory
OUTPATH = './results/replication/rf'

# params for rf regressor
rf_params = {
    "n_estimators": 20,
    "criterion": "mse",
    "max_features": None,
    "max_depth": 20,
    "min_samples_split": 2,
    "bootstrap": True,
    "random_state": 123
}


def do_experiment(hour, site, **dataset_args):
    query = Query(target_hour=hour, site=site, **dataset_args)
    dataset = Dataset(query=query)
    X_train, X_test, y_train, y_test = \
        train_test_split(dataset.examples, dataset.labels,
                         test_size=0.20, random_state=123)
    regressor = RandomForestRegressor(**rf_params)
    regressor.fit(X_train, y_train)
    predictions = regressor.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    return mae


if __name__ == '__main__':
    # iterate over all sites
    for site_name in sites.get_names():
        print("Working on site %s" % site_name)
        # construct TextTable for writing out results
        table = Texttable()
        table.set_cols_align(["c", "c", "c", "c", "c", "c", "c", "c"])
        table.header(["Hour", "gaemn only", "gaemn+window",
                      "gaemn + window + single-cell",
                      "gaemn + window + multicell", "NAM Only",
                      "% decrease", "% decrease (NAM Only)"])

        # do an experiment for each hour and each dataset
        for hour in list(range(1, 37)):
            dataset_components = {
                'gaemn': True,
                'window': True,
                'rap_cell': hour <= 18,
                'rap_grid': hour <= 18,
                'nam_cell': hour > 18,
                'nam_grid': hour > 18,
                'start_date': '2011-06-22' if hour <= 18 else '2003-01-01',
                'end_date': '2012-04-30 23:45:00' if hour <= 18 else '2006-01-01'
            }
            print("Hour %d" % hour)
            all_attr_mae = do_experiment(
                hour, site_name, gaemn=True,
                start_date=dataset_components['start_date'],
                end_date=dataset_components['end_date'],
            )
            window_mae = do_experiment(
                hour, site_name, gaemn=True, window=True,
                start_date=dataset_components['start_date'],
                end_date=dataset_components['end_date'],
            )
            singlecell_mae = do_experiment(
                hour, site_name, gaemn=True, window=True,
                nam_cell=dataset_components['nam_cell'],
                rap_cell=dataset_components['rap_cell'],
                start_date=dataset_components['start_date'],
                end_date=dataset_components['end_date'],
            )
            multicell_mae = do_experiment(
                hour, site_name, gaemn=True, window=True,
                nam_cell=dataset_components['nam_cell'],
                rap_cell=dataset_components['rap_cell'],
                nam_grid=dataset_components['nam_grid'],
                rap_grid=dataset_components['rap_grid'],
                start_date=dataset_components['start_date'],
                end_date=dataset_components['end_date'],
            )
            nam_only = do_experiment(
                hour, site_name, gaemn=False, window=False,
                nam_cell=dataset_components['nam_cell'],
                rap_cell=dataset_components['rap_cell'],
                nam_grid=dataset_components['nam_grid'],
                rap_grid=dataset_components['rap_grid'],
                start_date=dataset_components['start_date'],
                end_date=dataset_components['end_date'],)
            pct_improvement = (window_mae - multicell_mae) * 100 / window_mae
            pct_improvement_nam = (window_mae - nam_only) * 100 / window_mae
            table.add_row(
                [hour, all_attr_mae, window_mae, singlecell_mae,
                 multicell_mae, nam_only, pct_improvement, pct_improvement_nam])

        # output the table to a file:
        if not os.path.exists(OUTPATH):
            os.makedirs(OUTPATH)
        outfilepath = os.path.join(OUTPATH, site_name+".txt")
        with open(outfilepath, 'w') as outfile:
            print(site_name.capitalize(), file=outfile)
            print(table.draw(), file=outfile)

    print("Done!")
