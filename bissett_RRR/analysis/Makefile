# Makefile for IID analyses

# variables

# set to your username if you wish to push custom version to a different dockerhub acct
DOCKER_USERNAME = poldrack

# code to check environment variables
# from https://stackoverflow.com/questions/4728810/makefile-variable-as-prerequisite

guard-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set"; \
		exit 1; \
	fi

# from https://stackoverflow.com/questions/18136918/how-to-get-current-relative-directory-of-your-makefile

current_dir = $(shell pwd)
backone = `dirname \`pwd\``

# testing functions

test:
	pytest

check-style:
	flake8 --show-source  | tee stylecheck.out

# get list of R packages needed by checkpoint
get-R-packages:
	cat *.Rmd | grep library >| R_libraries.R


run-organize:
	python organize_data_DirectReplication1.py

run-preprocess:
	python preprocess_data_DirectRep1.py


# commands to run analyses via docker

run-all: run-organize run-preprocess


run-stats: guard-DOCKER_USERNAME get-R-packages
        docker run -v $(current_dir):/analysis $(DOCKER_USERNAME)/openscience-example Rscript -e 'library(knitr);library(rmarkdown); rmarkdown::render("/analysis/analysis/ReplicationAnalyses.Rmd", "html_document", output_dir = "/analysis/figures")'


#run-Preprocesss: guard-DOCKER_USERNAME 
#	docker run -e "DATA_URL=$(DATA_URL)" -v $(current_dir):/analysis -v $(NARPS_BASEDIR):/data $(DOCKER_USERNAME)/iid-analysis /bin/bash -c "source /etc/fsl/5.0/fsl.sh;python /analysis/PreprocessMaps.py"

run-Analyze: guard-DOCKER_USERNAME
	docker run -v $(current_dir):/analysis -v $(NARPS_BASEDIR):/data $(DOCKER_USERNAME)/iid-analysis /bin/bash -c "source /etc/fsl/5.0/fsl.sh;python /analysis/AnalyzeMaps.py" 


# commands for building and testing docker image

docker-build: guard-DOCKER_USERNAME
	docker build -t $(DOCKER_USERNAME)/openscience-example .

docker-deploy: docker-login docker-upload

docker-login: guard-DOCKER_USERNAME guard-DOCKER_PASSWORD
	docker login --username=$(DOCKER_USERNAME) --password=$(DOCKER_PASSWORD)

# add -p 8888:8888 for jupyter
shell: guard-DOCKER_USERNAME
	docker run -p 9994:9994 -it --entrypoint=bash -v $(current_dir)/..:/analysis $(DOCKER_USERNAME)/openscience-example


jupyter: guard-DOCKER_USERNAME
	docker run -it -p 9994:9994 --entrypoint /usr/local/bin/jupyter -v $(current_dir)/..:/analysis $(DOCKER_USERNAME)/openscience-example lab --ip=0.0.0.0 --port=9994 --allow-root

singularity-shell:
	PYTHONPATH="" singularity shell --cleanenv docker://poldrack/jupyter-python-r
