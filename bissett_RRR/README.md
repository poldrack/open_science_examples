## Inhibition-induced devaluation

This repository includes data and code to fully reproduce analyses for Bissett et al's attempted replication of [Wessel et al. (2014)](https://pubmed.ncbi.nlm.nih.gov/25313953/).


### Data reorganization

Original source data (downloaded from https://osf.io/x38aj/files/) are located in raw_data/source_data.

These are converted to a format similar to [Psych-DS](https://psych-ds.github.io/) using ```analysis/organize_data_study-1.py```.

The resulting reorganized data are located in raw_data/study-1, with a separate tab-separated value (.tsv) file for each subject.

### Preprocessing

The data are subsequently preprocessed in order to obtain summary results for each subject for the stop signal and auction tasks, using ```analysis/preprocess_data_study-1.py```.

The resulting preprocessed data are saved to ```processed_data/study-1_task-stop_data.tsv``` and ```processed_data/study-1_task-auction_data.tsv```.

### Statistical analysis

The primary hypothesis of interest for this study is the effect of inhibitory training on subsequent valuation in the auction phase.  This is tested using a mixed effects model, implemented using the [statsmodels](https://www.statsmodels.org/stable/index.html) Python package in ```analysis/ReplicationAnalyses.ipynb```.



### Reproducible execution

In order to ensure exact reproducibility of the analyses, we have implemented a Docker container that includes all of the necessary libraries for executing the steps outlined above.  To run the entire processing stream:

1. [Install the Docker client](https://docs.docker.com/get-docker/) on your computer.
2. Run the analysis using the following command: ```make run-all```


### Software tests

We have included a test for the ```get_SSRT()``` function, which is used to compute stop-signal reaction time.  This test repeatedly generates data with a known SSRT value, and then assesses the accuracy of the function's estimates.  The test succeeds if the estimated SSRT values are correlated > 0.98 with the values used to generate the data.