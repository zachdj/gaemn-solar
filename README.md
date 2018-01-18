# solarrad
Machine Learning models for predicting solar radiation from historical solar and 
weather forecast data.

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

After the environment has been activated, the python files can be run like normal.  e.g.
```python main.py```

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

## Versioning

This project uses the [GitFlow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) workflow
to organize branches and "releases".

## Authors

* [**Zach Jones**](https://github.com/zachdj)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
