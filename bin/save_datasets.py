""" Saves a selection of datasets as csv files """

from solardata.Dataset import Dataset
from solardata.query import Query

for hour in [1, 12, 24]:
    gaemn_query = Query(target_hour=hour, site='griffin', gaemn=True, window=False, nam_cell=False, nam_grid=False)
    gaemn_ds = Dataset(query=gaemn_query)
    gaemn_window_query = Query(target_hour=hour, site='griffin', gaemn=True, window=True, nam_cell=False, nam_grid=False)
    gaemn_window_ds = Dataset(query=gaemn_window_query)

    gaemn_ds.dump_to_csv(directory="../tmp/datasets", filename='gaemn_%d' % hour)
    gaemn_window_ds.dump_to_csv(directory="../tmp/datasets", filename='gaemn_window_%d' % hour)
