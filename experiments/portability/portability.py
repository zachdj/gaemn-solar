""" Experiment which tests the geographical portability of RF models

one_vs_rest - trains on one site and tests on all the others
rest_vs_one - traines on 4 sites and evaluates the one left out

"""

import logging
import sys
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

import solardata.sites as sites
from solardata.query import Query
from solardata.Dataset import Dataset

logger = logging.getLogger(__name__)


# params for rf regressor
_RF_PARAMS = {
    "n_estimators": 20,
    "criterion": "mse",
    "max_features": None,
    "max_depth": 20,
    "min_samples_split": 2,
    "bootstrap": True,
    "random_state": 123
}


def one_vs_rest(include_gaemn=True):
    logger.info('Running experiment ONE vs REST')
    for site in sites.get_names():
        logger.info(f'Training on site {site}')
        for hour in (1, 24):
            logger.info(f'for hour {hour}')
            dataset_components = {
                'target_hour': hour,
                'gaemn': include_gaemn,
                'window': include_gaemn,
                'rap_cell': hour <= 18,
                'rap_grid': hour <= 18,
                'nam_cell': hour > 18,
                'nam_grid': hour > 18,
                'start_date': '2011-06-22' if hour <= 18 else '2003-01-01',
                'end_date': '2012-04-30 23:45:00' if hour <= 18 else '2006-01-01'
            }
            site_query = Query(site=site, **dataset_components)
            site_ds = Dataset(query=site_query)

            rf = RandomForestRegressor(**_RF_PARAMS)
            rf.fit(site_ds.examples, site_ds.labels)

            other_site_queries = [
                Query(site=other_site, **dataset_components)
                for other_site in sites.get_names()
                if other_site != site
            ]
            other_site_ds = [
                Dataset(query=os_query) for os_query in other_site_queries
            ]
            test_x = np.concatenate(
                [ds.examples for ds in other_site_ds],
                axis=0
            )
            test_y = np.concatenate(
                [ds.labels for ds in other_site_ds],
                axis=0
            )

            y_pred = rf.predict(test_x)
            mae = mean_absolute_error(test_y, y_pred)
            print(site, hour, mae)


def rest_vs_one(include_gaemn=True):
    logger.info('Running experiment REST vs ONE')
    for site in sites.get_names():
        logger.info(f'Testing on site {site}')
        for hour in (1, 24):
            dataset_components = {
                'target_hour': hour,
                'gaemn': include_gaemn,
                'window': include_gaemn,
                'rap_cell': hour <= 18,
                'rap_grid': hour <= 18,
                'nam_cell': hour > 18,
                'nam_grid': hour > 18,
                'start_date': '2011-06-22' if hour <= 18 else '2003-01-01',
                'end_date': '2012-04-30 23:45:00' if hour <= 18 else '2006-01-01'
            }
            other_site_queries = [
                Query(site=other_site, **dataset_components)
                for other_site in sites.get_names()
                if other_site != site
            ]
            other_site_ds = [
                Dataset(query=os_query) for os_query in other_site_queries
            ]
            train_x = []
            train_y = []
            for ds in other_site_ds:
                # resample so that the size of the training sets are the same
                # as in one_vs_rest
                sample_indices = np.random.random_integers(
                    0, len(ds.examples)-1, len(ds.examples) // 4)
                train_x.append(ds.examples[sample_indices])
                train_y.append(ds.labels[sample_indices])

            train_x = np.concatenate(
                [x for x in train_x],
                axis=0
            )
            train_y = np.concatenate(
                [y for y in train_y],
                axis=0
            )

            rf = RandomForestRegressor(**_RF_PARAMS)
            rf.fit(train_x, train_y)

            site_query = Query(site=site, **dataset_components)
            site_ds = Dataset(query=site_query)

            y_true = site_ds.labels
            y_pred = rf.predict(site_ds.examples)

            mae = mean_absolute_error(y_true, y_pred)
            print(site, hour, mae)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(message)s')
    one_vs_rest()
    rest_vs_one()

    print('\n************************\n'
          'Re-running experiments with NAM-only dataset')
    one_vs_rest(include_gaemn=False)
    rest_vs_one(include_gaemn=False)
