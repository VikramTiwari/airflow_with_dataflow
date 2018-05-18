# Airflow with Dataflow

## Requirements
- Python 2
- Google Cloud with Composer and Dataflow activated

## Setup

```
# this will create a virtual environment without affecting anything on your system
virtualenv -p=python2 dataflow

# activate virual environment
source dataflow/bin/activate

# install necessary packages
pip install --upgrade setuptools apache-beam
pip install --upgrade apache-beam[gcp]
pip install -r requirements.txt
```

## Running dataflow jobs

```
# build the exta package
python setup.py sdist --formats=gztar

# testing locally
python etl.py --runner=DirectRunner --setup-file=./setup.py --requirements-file=./requirements.txt --extra_package=./dist/Common-1.0.0.tar.gz --start_date=2018-01-01 --end_date:2018-01-02

# running on dataflow
python etl.py --runner=DataflowRunner --setup-file=./setup.py --requirements-file=./requirements.txt --extra_package=./dist/Common-1.0.0.tar.gz --start_date=2018-01-01 --end_date:2018-01-02
```

## To run this from airflow
- TODO: add details


## Extra guides

### Converting a local package for dataflow's extra_package

- Create `setup.py` outside of local package directory with following content

```
from setuptools import setup, find_packages

setup(
    name="Common",
    version="1.0.0",
    install_requires=['pandas==0.22.0', 'numpy==1.14.2'],
    author="Vikram Tiwari",
    author_email="vikramtheone1@gmail.com",
    description=("Custom python utils needed for dataflow cloud runner"),
    packages=find_packages(),
    package_data={
        "Common": [".credentials/*.json"]
    },
    include_package_data=True)
````

- Build package

```
python setup.py sdist --formats=gztar
```

