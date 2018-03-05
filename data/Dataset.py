import csv
import os
import numpy as np
import pandas as pd


def generate_from_csv(filepath, name=None):
    """
    Reads a dataset from a csv file at the given location
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


# def generate_from_query(target_hour=1, site_id=115, ):



class Dataset(object):
    def __init__(self, name, X, y=None, attr_labels=None):
        """
        Object-oriented interface representing a dataset
        X is an array of examples, where each example has n attributes
        y is an (optional) array of labels or values

        :param name: a logical name for this dataset
        :param X: an array of data points without labels
        :param y: the labels corresponding to X
        :param attr_labels: labels for the columns of X and y
        """
        self.name = str(name)
        self.data = X
        self.labels = y

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

        # assemble data into csv form
        labels = np.reshape(self.labels, (len(self.labels), 1))
        data = np.append(self.data, labels, axis=1)
        print(data)

        filepath = os.path.join(directory, filename)
        with open(filepath, 'w') as outfile:
            writer = csv.writer(outfile, delimiter=",")
            for example in data:
                writer.writerow(example)

        return filepath
