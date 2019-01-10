""" Saves some datasets as csv files so they can be opened elsewhere """

from solarrad import Dataset

for hour in [1, 12, 24]:
    gaemn_ds = Dataset.generate_from_query(target_hour=hour, site_id=115, gaemn=True, window=False, nam_cell=False, nam_grid=False)
    gaemn_window_ds = Dataset.generate_from_query(target_hour=hour, site_id=115, gaemn=True, window=True, nam_cell=False, nam_grid=False)

    gaemn_ds.write_to_file(directory="../data", filename='gaemn_%d' % hour)
    gaemn_window_ds.write_to_file(directory="../data", filename='gaemn_window_%d' % hour)
