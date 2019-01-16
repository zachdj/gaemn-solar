""" Experiments with persistence models """

import logging
import mysql.connector
import sys
from texttable import Texttable

from sklearn.metrics import mean_absolute_error

import solardata.config
import solardata.sites as sites

logger = logging.getLogger(__name__)


def current_value():
    """ Computes MAE using current-value persistence model for the five GAEMN sites"""

    gaemn_sites = sites.SITES
    columns = ['hour']
    for site in gaemn_sites:
        columns.append(site)
    columns.append('all')
    table = Texttable()
    table.set_cols_align(['c', 'c', 'c', 'c', 'c', 'c', 'c'])
    table.header(columns)

    # open connection
    db_config = solardata.config.to_dict()
    cnx = mysql.connector.connect(**db_config)

    logger.debug('Computing MAE for current-value persistence model')
    hr_1_query = "SELECT sr.dateandtime, sr.sr AS current_val, sr.sr1 AS future_val FROM solarradiation sr " \
                 "INNER JOIN gribprediction gp ON gp.SolarRadiationID=sr.id AND (gp.Datasource='rap' OR gp.Datasource='rapinterpolation') " \
                 "AND gp.HoursAhead=1 AND gp.cell='' and gp.SiteID=sr.siteID " \
                 "WHERE sr.dateandtime BETWEEN '2011-06-22' AND '2012-04-30 23:45:00' and sr.SiteID IN %s " \
                 "ORDER BY sr.dateandtime " \
                 "LIMIT 200000;"

    hr_24_query = "SELECT sr.dateandtime, sr.sr AS current_val, sr.sr24 AS future_val FROM solarradiation sr " \
                  "INNER JOIN gribprediction gp ON gp.SolarRadiationID=sr.id AND (gp.Datasource='NAM' OR gp.Datasource='NAMinterpolation') " \
                  "AND gp.HoursAhead=24 AND gp.cell='' and gp.SiteID=sr.siteID " \
                  "WHERE sr.dateandtime BETWEEN '2003-01-01' AND '2006-01-01' and sr.SiteID IN %s " \
                  "ORDER BY sr.dateandtime " \
                  "LIMIT 200000;"

    hr_1_maes = []
    hr_24_maes = []
    # compute error for each site
    for site in gaemn_sites:
        logger.debug(f'Computing MAE for {site}...')

        # finish the query's WHERE clause
        site_id = sites.get_site_id_by_name(site)
        site_tuple = f'({site_id})'
        site_query_1 = hr_1_query % site_tuple
        site_query_24 = hr_24_query % site_tuple

        # get 1_hr records
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(site_query_1)
        y_true, y_pred = [], []
        for record in cursor:
            y_pred.append(float(record['current_val']))
            y_true.append(float(record['future_val']))

        # compute MAE
        mae_1 = mean_absolute_error(y_true, y_pred)
        hr_1_maes.append(mae_1)
        logger.debug(f'1-hr MAE for {site} is {mae_1}')

        # get 24_hr records
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(site_query_24)
        y_true, y_pred = [], []
        for record in cursor:
            y_pred.append(float(record['current_val']))
            y_true.append(float(record['future_val']))

        # compute MAE
        mae_24 = mean_absolute_error(y_true, y_pred)
        hr_24_maes.append(mae_24)
        logger.debug(f'24-hr MAE for {site} is {mae_24}')

    # compute error for all sites combined
    logger.debug(f'Computing MAE for all sites...')

    mae_1 = sum(hr_1_maes) / len(hr_1_maes)
    hr_1_maes.append(mae_1)
    logger.debug(f'1-hr MAE across all sites is {mae_1}')
    table.add_row(['1'] + hr_1_maes)

    mae_24 = sum(hr_24_maes) / len(hr_24_maes)
    hr_24_maes.append(mae_24)
    logger.debug(f'24-hr MAE across all sites is {mae_24}')
    table.add_row(['24'] + hr_24_maes)

    logger.info('MAEs using current-value persistence model')
    logger.info(table.draw())

    cnx.close()


def historic_value():
    """ Computes MAE using historic-value persistence model for the five sites

    The historic-valuie persistence model uses the average solar radiation value for the desired datetime
    computed from 2003-2013

    """
    gaemn_sites = sites.SITES
    columns = ['hour']
    for site in gaemn_sites:
        columns.append(site)
    columns.append('all')
    table = Texttable()
    table.set_cols_align(['c', 'c', 'c', 'c', 'c', 'c', 'c'])
    table.header(columns)

    logger.debug('Computing MAE for historic-value persistence model')
    table.header(columns)

    # open connection
    db_config = solardata.config.to_dict()
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor(dictionary=True)

    # compute historic averages
    logger.debug('Computing historic averages')
    historic_avgs = {}
    cursor.execute('SELECT AVG(sr) as avg_value, day, time from solarradiation GROUP BY day, time;')
    for record in cursor:
        day, time = record['day'], record['time']
        day_time = f'{day}-{time}'
        avg_val = float(record['avg_value'])
        historic_avgs[day_time] = avg_val

    # queries for true values
    hr_1_query = "SELECT sr.dateandtime, sr.day as computed_day, (sr.time+100) as computed_time, sr.sr1 AS true_val " \
                 "FROM solarradiation as sr " \
                 "INNER JOIN gribprediction gp ON gp.SolarRadiationID=sr.id AND (gp.Datasource='rap' OR gp.Datasource='rapinterpolation') " \
                 "AND gp.HoursAhead=1 AND gp.cell='' AND gp.SiteID=sr.siteID " \
                 "WHERE sr.dateandtime BETWEEN '2011-06-22' AND '2012-04-30 23:45:00' and sr.SiteID IN %s " \
                 "ORDER BY sr.dateandtime " \
                 "LIMIT 100000;"

    hr_24_query = "SELECT sr.dateandtime, (sr.day+1) as computed_day, sr.time as computed_time, sr.sr24 AS true_val " \
                  "FROM solarradiation as sr " \
                  "INNER JOIN gribprediction gp ON gp.SolarRadiationID=sr.id AND (gp.Datasource='NAM' OR gp.Datasource='NAMinterpolation')  " \
                  "AND gp.HoursAhead=24 AND gp.cell='' AND gp.SiteID=sr.siteID " \
                  "WHERE sr.dateandtime BETWEEN '2003-01-01' AND '2006-01-01' and sr.SiteID IN %s " \
                  "ORDER BY sr.dateandtime " \
                  "LIMIT 100000;"

    hr_1_maes = []
    hr_24_maes = []
    for site in gaemn_sites:
        logger.debug(f'Computing MAE for {site}')

        # finish the query's WHERE clause
        site_id = sites.get_site_id_by_name(site)
        site_tuple = f'({site_id})'
        site_query_1 = hr_1_query % site_tuple
        site_query_24 = hr_24_query % site_tuple

        # get 1-hr records
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(site_query_1)
        y_true, y_pred = [], []
        for record in cursor:
            day, time = record['computed_day'], record['computed_time']
            key = f'{day}-{time}'
            true_val = float(record['true_val'])
            y_true.append(true_val)
            if key in historic_avgs:
                y_pred.append(historic_avgs[key])
            else:
                y_pred.append(0)

        # compute 1-hr MAE
        mae_1 = mean_absolute_error(y_true, y_pred)
        hr_1_maes.append(mae_1)
        logger.debug(f'1-hr MAE for {site} is {mae_1}')

        # get 24-hr records
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(site_query_24)
        y_true, y_pred = [], []
        for record in cursor:
            day, time = record['computed_day'], record['computed_time']
            key = f'{day}-{time}'
            true_val = float(record['true_val'])
            y_true.append(true_val)
            if key in historic_avgs:
                y_pred.append(historic_avgs[key])
            else:
                y_pred.append(0)

        # compute 24-hr MAE
        mae_24 = mean_absolute_error(y_true, y_pred)
        hr_24_maes.append(mae_24)
        logger.debug(f'24-hr MAE for {site} is {mae_24}')

    # compute error for all sites combined
    logger.debug(f'Computing MAE for all sites...')

    mae_1 = sum(hr_1_maes) / len(hr_1_maes)
    hr_1_maes.append(mae_1)
    logger.debug(f'1-hr MAE across all sites is {mae_1}')
    table.add_row(['1'] + hr_1_maes)

    mae_24 = sum(hr_24_maes) / len(hr_24_maes)
    hr_24_maes.append(mae_24)
    logger.debug(f'24-hr MAE across all sites is {mae_24}')
    table.add_row(['24'] + hr_24_maes)

    logger.info('MAEs using historic-value persistence model')
    logger.info(table.draw())

    cnx.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(levelname)s:%(name)s:%(asctime)s\n%(message)s')

    current_value()
    historic_value()
