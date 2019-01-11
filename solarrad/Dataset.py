import csv
import os
import numpy as np
import pandas as pd
import mysql.connector

from solarrad.query import build as build_query
import solarrad.config as config


def generate_from_csv(filepath, name=None):
    """ Reads a dataset from a csv file at the given location

    :param filepath: the location of the csv file on the local filesystem
    :param name: (Optional) logical name for the dataset.  Defaults to the filepath
    :return: Dataset object representing the contents of the csv file
    """
    df = pd.read_csv(filepath, sep=',')
    X = df[df.columns.tolist()[:-1]].values
    y = df[df.columns.tolist()[-1]].values
    column_names = list(df.axes[1])

    if name is None:
        name = filepath

    return Dataset(name, X, y, attr_labels=column_names)


def generate_from_query(target_hour=1, site_id=115, gaemn=True, window=False, nam_cell=False, nam_grid=False,
                        start_date='2011-06-22', end_date='2012-04-30 23:45:00', name=None):

    X = []  # attributes
    y = []  # target

    # establish connection to mySQL database
    db_config = config.to_dict()
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()

    # build and execute the query
    query_string = build_query(target_hour, site_id, gaemn, window, nam_cell, nam_grid, start_date, end_date)

    cursor.execute(query_string)
    attribute_names = [i[0] for i in cursor.description]
    for record in cursor:
        X.append(
            np.array(record[:-1]).astype(float)
        )
        y.append(float(record[-1]))
    cnx.close()

    if name is None:
        name = f'data_{target_hour}hour'
        if gaemn: name += '_gaemn'
        if window: name += '_window'
        if nam_cell: name += '_cell'
        if window: name += '_multi'

    return Dataset(name, X, y, attr_labels=attribute_names)


class Dataset(object):
    def __init__(self, name, X, y=None, attr_labels=None):
        """
        Object-oriented interface representing a dataset
        X is an array of examples, where each example has n attributes
        y is an (optional) array of labels or values

        :param name: a logical name for this dataset
        :param X: an array of solarrad points without labels
        :param y: the labels corresponding to X
        :param attr_labels: labels for the columns of X and y
        """
        self.name = str(name)
        self.data = np.array(X)
        self.labels = np.array(y)
        self.attr_labels = attr_labels

    def write_to_file(self, directory, filename=None):
        """
        Writes the dataset as a csv file to <filename>.csv in the given directory
        If filename is None, the the Dataset name will be used as the filename
        :param directory: the directory to write this dataset
        :param filename: the filename that this dataset will be written to
        :return: the full path of the output file
        """
        if filename is None:
            filename = self.name + ".csv"
        else:
            filename += ".csv"

        # ensure directory exists
        if not os.path.exists(directory):
            os.makedirs(directory)

        # assemble solarrad into csv form
        labels = np.reshape(self.labels, (len(self.labels), 1))
        data = np.append(self.data, labels, axis=1)

        filepath = os.path.join(directory, filename)
        with open(filepath, 'w') as outfile:
            writer = csv.writer(outfile, delimiter=",")
            # write a header row if the attribute names are known
            if self.attr_labels is not None:
                writer.writerow(self.attr_labels)

            # write a line for each example
            for example in data:
                writer.writerow(example)

        return filepath
