# Inhibition-induced devaluation

![Python application](https://github.com/poldrack/open_science_examples/workflows/Python%20application/badge.svg)

This repository includes data and code to fully reproduce analyses for Bissett et al's attempted replication of [Wessel et al. (2014)](https://pubmed.ncbi.nlm.nih.gov/25313953/).  The dataset here (referred to as ``study-1``) was a preliminary replication attempt using an implementation of the published task developed by Bissett and colleagues; the materials and code used to administer this task are in [materials/DirectReplication1Code][materials/DirectReplication1Code).  

## Data reorganization

Original source data (downloaded from https://osf.io/x38aj/files/) are located in [data/primary_data/source_data](data/primary_data/source_data).

These are converted to a format similar to [Psych-DS](https://psych-ds.github.io/) using [analysis/organize_data.py](analysis/organize_data.py).

The resulting reorganized data are located in [data/primary_data/study-1](data/primary_data/study-1) , with a separate tab-separated value (.tsv) file for each subject.

## Preprocessing

The data are subsequently preprocessed in order to obtain summary results for each subject for the stop signal and auction tasks, using [analysis/preprocess_data.py](analysis/preprocess_data.py)

The resulting preprocessed data are saved to:

- stop task: [data/processed_data/study-1_task-stop_data.tsv](data/study-1_task-stop_data.tsv)
- auction task: [data/processed_data/study-1_task-auction_data.tsv](data/study-1_task-auction_data.tsv).

## Statistical analysis

The primary hypothesis of interest for this study is the effect of inhibitory training on subsequent valuation in the auction phase.  This is tested using a mixed effects model, implemented using the [statsmodels](https://www.statsmodels.org/stable/index.html) Python package in [analysis/ReplicationAnalyses.ipynb](analysis/ReplicationAnalyses.ipynb).

The results are output to [analysis/ReplicationAnalyses.html](analysis/ReplicationAnalyses.html).

## Reproducible execution

In order to ensure exact reproducibility of the analyses, we have implemented a Docker container that includes all of the necessary libraries for executing the steps outlined above.  To run the entire processing stream:

1. [Install the Docker client](https://docs.docker.com/get-docker/) on your computer.
2. From the analysis subdirectory, run the analysis using the following command: ```make run-all```

The Docker image is built using [analysis/Dockerfile](analysis/Dockerfile). If you run the commands without building the Dockerfile locally, then the latest image will be downloaded from [Dockerhub](https://hub.docker.com/r/poldrack/openscience-example).  If you wish to build it locally, you should first change the ```DOCKER_USERNAME``` variable in [analysis/Makefile](analysis/Makefile) to your own Dockerhub username, so that all of the commands will use your own version and you will be able to push it back to Dockerhub if you wish.  You can then build it from within the analysis directory using ```make docker-build```.


## Software tests

We have included a test for the ```get_SSRT()``` function, which is used to compute stop-signal reaction time.  This test repeatedly generates data with a known SSRT value, and then assesses the accuracy of the function's estimates.  The test succeeds if the estimated SSRT values are correlated > 0.98 with the values used to generate the data.  The code that implements this test can be found at [analysis/test_SSRT.py](analysis/test_SSRT.py).

To run the test, issue the following command from the analysis subdirectory: ```make run-test```

This test is automatically performed whenever a new commit is made to the repository, using [Github Actions](https://help.github.com/en/actions).  See the setup file for this automated test [here](../.github/workflows/python-app.yml).


## Automated workflow execution

TBD


## Sharing of results

TBD
