import csv
import os
import numpy as np
import pandas as pd
import mysql.connector

from solardata.query import Query
import solardata.config as config


class Dataset(object):
    def __init__(self, name=None, query=None, csv_file=None):
        """ Represents a dataset of (example, label) pairs

        Datasets can be initialized using a SQL query, which will be executed against the database specified by the
        `config.db.json` file.

        Datasets can be initialized by passing the full path to a csv file via the `csv_file` argument.

        If both the `query` and `csv_file` arguments are provided, then the dataset will be initialized using the
        SQL query and ignore the csv file.

        If neither of the `query` or `csv_file` arguments are provided, the dataset will be empty.

        Args:
            name (str): logical name for the dataset
            query (Query or None): if set, intialize the dataset by executing the provided solardata.query.Query
            csv_file (str or None): if set, initialize the dataset using the csv file at this location
        """
        name = name
        examples = []
        labels = []
        column_names = []

        if query is not None:
            # establish connection to mySQL database
            db_config = config.to_dict()
            cnx = mysql.connector.connect(**db_config)

            # execute query
            cursor = cnx.cursor()
            cursor.execute(str(query))
            column_names = [i[0] for i in cursor.description]
            for record in cursor:
                examples.append(
                    np.array(record[:-1]).astype(float)
                )
                labels.append(float(record[-1]))
            cnx.close()

            if name is None:
                name = f'data_{query.target_hour}hour'
                if query.components['gaemn']: name += '_gaemn'
                if query.components['window']: name += '_window'
                if query.components['nam_cell']: name += '_nam'
                if query.components['nam_grid']: name += '_grid'

        elif csv_file is not None:
            dataframe = pd.read_csv(csv_file, sep=',')
            examples = dataframe[dataframe.columns.tolist()[:-1]].values
            labels = dataframe[dataframe.columns.tolist()[-1]].values
            column_names = list(dataframe.axes[1])

            if name is None:
                name = csv_file

        self.name = str(name)
        self.examples = np.array(examples)
        self.labels = np.array(labels)
        self.column_names = column_names

    def dump_to_csv(self, directory, filename=None):
        """ Dumps the dataset to a csv file

        Args:
            directory (str): location where the dataset will be written
            filename (str or None): if set, the output file will be named <filename>.csv

        Returns:
            str: path to the output file

        """
        if filename is None:
            filename = self.name + ".csv"
        else:
            filename += ".csv"

        # ensure directory exists
        if not os.path.exists(directory):
            os.makedirs(directory)

        # reshape data to be tabular
        labels = np.reshape(self.labels, (len(self.labels), 1))
        data = np.append(self.examples, labels, axis=1)

        filepath = os.path.join(directory, filename)
        with open(filepath, 'w') as outfile:
            writer = csv.writer(outfile, delimiter=",")
            # write a header row if the attribute names are known
            if len(self.column_names) > 0:
                writer.writerow(self.column_names)

            # write a line for each example
            for example in data:
                writer.writerow(example)

        return filepath
