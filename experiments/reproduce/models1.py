""" Trains several different types of ML models against dataset of GAEMN weather wariables for 1-hour prediction """

import logging
import sys
import time

from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.tree import DecisionTreeRegressor, ExtraTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from texttable import Texttable

from solardata.query import Query
from solardata.Dataset import Dataset

logger = logging.getLogger(__name__)


def main():
    logger.info(f'Computing MAE for set of 1-hour models')

    table_columns = ['Machine Learning Method', 'MAE (watts/m2)', 'Time (s)']
    table = Texttable()
    table.set_cols_align(['c', 'c', 'c'])
    table.header(table_columns)

    logger.debug('Generating query...')
    query = Query(target_hour=1, site='griffin', gaemn=True, window=False, nam_cell=False, nam_grid=False)
    logger.debug('Query: \n{query}')
    logger.debug('Constructing dataset from query')
    ds = Dataset(name='1hr-gaemn-data', query=query)
    X_train, X_test, y_train, y_test = train_test_split(ds.examples, ds.labels, test_size=0.20, random_state=123)

    models = {
        'Linear Regression': LinearRegression(),
        'Multilayer Perceptron': MLPRegressor(
            hidden_layer_sizes=(57,),
            activation='relu',
            solver='adam',
            batch_size=100,
            learning_rate='constant',
            learning_rate_init=0.3,
            momentum=0.2,
            random_state=123,
        ),
        'M5 Model Tree': DecisionTreeRegressor(
            min_samples_leaf=4,
            random_state=123,
        ),
        'Random Tree': ExtraTreeRegressor(
            max_features='log2',
            min_samples_leaf=4,
            random_state=123,
        ),
        'Random Forest': RandomForestRegressor(
            n_estimators=100,
            max_features='log2',
            random_state=123,
        )

    }

    for model_name in models:
        logger.debug(f'Training model {model_name}...')
        start_time = time.time()
        model = models[model_name]
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        end_time = time.time()
        time_elapsed = end_time - start_time

        table.add_row([model_name, mae, time_elapsed])

    logger.info(table.draw())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(message)s')
    main()
