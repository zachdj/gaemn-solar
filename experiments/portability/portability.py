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


def one_vs_rest():
    logger.info('Running experiment ONE vs REST')
    for site in sites.get_names():
        logger.info(f'Training on site {site}')
        for hour in (1, 24):
            logger.info(f'for hour {hour}')
            dataset_components = {
                'target_hour': hour,
                'gaemn': True,
                'window': True,
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


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(message)s')
    one_vs_rest()
