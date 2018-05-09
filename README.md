# GAEMN-Solar
Machine Learning models for predicting solar radiation using [GAEMN](http://www.georgiaweather.net/) weather data
and [NAM](https://www.ncdc.noaa.gov/data-access/model-data/model-datasets/north-american-mesoscale-forecast-system-nam)
weather forecasts.

## History

Georgia Power has installed a solar farm near the University of Georgia's campus.  However, its difficult to use
the farm effectively without a reliable prediction of the expected energy output.  A team of researchers at UGA have
been working to develop predictive models using machine learning.

[Sam Sanders, et al.](https://ieeexplore.ieee.org/abstract/document/8260680/)
trained Random Forest regressors to predict observed solar radiation 1 and 24 hours into the future.
He showed that prediction accuracy can be improved by incorporating a 24-hour window of radiation 
observations and by including a current weather forecast.

The purpose of this project is 3-fold:
    
1. Replicate Sanders' results
2. Extend the work temporally and ensure that results hold for every hour up to a 36 hour prediction
3. Make the epxeriments more easily replicable

### My Contributions

Available data is stored in a MySQL database.  It includes weather observations from the
[Georgia Automated  Environmental Monitoring Network](http://www.georgiaweather.net/) (GAEMN) and
weather predictions from the North American Mesoscale Forecast System (NAM) for five point locations in Georgia
for most of 2011 and some of 2012.
Previously, the datasets used for training/testing were extracted by manually running SQL queries and 
exporting the results as a CSV.  This project automates the data retrieval by dynamically constructing the SQL 
queries based on the desired dataset and time interval.  This alleviates the necessity of manually modifying and
running queries for each experiments

Previously, models were trained using the [WEKA](https://www.cs.waikato.ac.nz/ml/weka/) software.
This project ports Sanders' experiments to [scikit-learn](http://scikit-learn.org/stable/).
Although implementations differ slightly between WEKA and `scikit`, results were successfully replicated using
`scikit-learn` models.

Finally, Sanders' experiments were extended temporally.  This project builds models for every prediction hour 
extending to 36 hours in the future.  Results seem to hold regardless of the prediction hour.

### Weird observations

Originally, I was manually running `scikit` models on the CSV datasets extracted from Sam's SQL queries.
We were getting results _much_ worse than Sam.  After writing the module to extract data automatically, the
results matched.  It's possible I was using an old dataset or that pandas was ordering rows strangely.

In our experiments, adding a 24-hour window of past observations actually _hurts_ prediction accuracy.
This doesn't make much sense intuitively, since adding additional attributes shouldn't hurt the accuracy
of a properly trained tree ensemble.  It may be something odd with `scikit`'s splitting mechanics.

In our experiments, considering NAM data in isolation (that is, without GAEMN observations and without
a 24-hour window) produces superior prediction accuracy over any other dataset.  Sanders never
never trained a model using NAM-only data, so this result does not represent a deviation from expected
results but rather an interesting note.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for 
development and testing purposes.

### Prerequisites

This project uses Python to run experiments and build models.

Python installation and dependencies are managed using the [Conda](https://conda.io/docs/) 
package manager.  You'll need to install Conda to get setup.

### Installing Dependencies

The environment.yml file is used by Conda to create a virtual environment that includes all the project's dependencies (including Python!)

Navigate to the project directory and run the following command

```
conda env create
```

This will create a virtual environment named "solarrad".  Activate the virtual environment with the following command

```
conda activate solarrad
```

### Running experiments

Experiments are stored in the `experiments` subdirectory.  Currently, the only working experiment is 
`rf.py`.  After the environment has been activated, the experiments can be run as follows:

```$ python experiments/rf.py```

### Configuration variables
These scripts support user-defined configuration variables that tell the scripts the location of 
the text data and the location of the cluster on which to run.

The config.json file is ignored, so to get started, create a copy of ```config.example.json``` 
and rename it to ```config.json```.  The following variables should be set

* ```APP_NAME``` - If running on a cluster with a GUI, this name will show up while the job is running
   (defaults to 'zachdj-p0')
* ```CLUSTER_URI``` - The location of the cluster on which the jobs should be run (defaults to 'local')
* ```DATA_LOCATION``` - The local/remote directory, file name, or HDFS from which the text files should be read 
 (defaults to 'testdata')

## Built With

* [Python 3.6](https://www.python.org/)
* [Conda](https://conda.io/docs/) - Package Manager

## Authors

* [**Zach Jones**](https://github.com/zachdj)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
