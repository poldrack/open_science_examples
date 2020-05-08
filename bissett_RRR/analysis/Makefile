# Makefile for IID analyses

# variables
# use NARPS docker image from poldrack dockerhub
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
	pytest -q tests.py

check-style:
	flake8 --show-source  | tee stylecheck.out

# get list of R packages needed by checkpoint
get-R-packages:
	cat *.Rmd | grep library >| R_libraries.R


# commands to run analyses via docker

run-all: run-Preprocess run-Analyze

run-Preprocesss: guard-DOCKER_USERNAME 
	docker run -e "DATA_URL=$(DATA_URL)" -v $(current_dir):/analysis -v $(NARPS_BASEDIR):/data $(DOCKER_USERNAME)/iid-analysis /bin/bash -c "source /etc/fsl/5.0/fsl.sh;python /analysis/PreprocessMaps.py"

run-Analyze: guard-DOCKER_USERNAME
	docker run -v $(current_dir):/analysis -v $(NARPS_BASEDIR):/data $(DOCKER_USERNAME)/iid-analysis /bin/bash -c "source /etc/fsl/5.0/fsl.sh;python /analysis/AnalyzeMaps.py" 


# commands for building and testing docker image

docker-deploy: docker-login docker-upload

docker-login: guard-DOCKER_USERNAME guard-DOCKER_PASSWORD
	docker login --username=$(DOCKER_USERNAME) --password=$(DOCKER_PASSWORD)

# add -p 8888:8888 for jupyter
shell: guard-DOCKER_USERNAME
	docker run -p 9994:9994 -e "DATA_URL=$(DATA_URL)" -it --entrypoint=bash -v $(current_dir)/..:/analysis $(DOCKER_USERNAME)/jupyter-python-r


jupyter: guard-DOCKER_USERNAME
	docker run -it -p 9994:9994 --entrypoint /opt/conda/bin/jupyter -v $(current_dir)/..:/analysis $(DOCKER_USERNAME)/jupyter-python-r lab --ip=0.0.0.0 --port=9994 --allow-root

singularity-shell:
	PYTHONPATH="" singularity shell --cleanenv docker://poldrack/jupyter-python-r
