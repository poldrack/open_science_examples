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
parent_dir = $(shell dirname $(current_dir))

# testing functions

test:
	pytest

check-style:
	flake8 --show-source  | tee stylecheck.out

# remove all outputs
clean:
	-rm ReplicationAnalyses.html
	-rm ../data/*.tsv
	-rm ../data/primary_data/study-*/*tsv


# commands to run analyses via docker

run-all: run-organize run-preprocess run-stats

run-organize: guard-DOCKER_USERNAME
	docker run -v $(parent_dir):/analysis $(DOCKER_USERNAME)/openscience-example python analysis/organize_data.py -b /analysis

run-preprocess: guard-DOCKER_USERNAME
	docker run -v $(parent_dir):/analysis $(DOCKER_USERNAME)/openscience-example python analysis/preprocess_data.py -b /analysis

run-stats: guard-DOCKER_USERNAME
	docker run -v $(parent_dir):/analysis $(DOCKER_USERNAME)/openscience-example jupyter nbconvert --to html --execute analysis/ReplicationAnalyses.ipynb

run-test: guard-DOCKER_USERNAME
	docker run -v $(parent_dir):/analysis $(DOCKER_USERNAME)/openscience-example pytest /analysis/analysis


# commands for building and testing docker image

docker-build: guard-DOCKER_USERNAME
	docker build -t $(DOCKER_USERNAME)/openscience-example .

docker-deploy: docker-login docker-upload

docker-upload: guard-DOCKER_USERNAME
	docker push $(DOCKER_USERNAME)/openscience-example

docker-login: guard-DOCKER_USERNAME guard-DOCKER_PASSWORD
	docker login --username=$(DOCKER_USERNAME) --password=$(DOCKER_PASSWORD)

# add -p 8888:8888 for jupyter
shell: guard-DOCKER_USERNAME
	docker run -p 9994:9994 -it --entrypoint=bash -v $(current_dir)/..:/analysis $(DOCKER_USERNAME)/openscience-example

jupyter: guard-DOCKER_USERNAME
	docker run -it -p 9994:9994 --entrypoint /usr/local/bin/jupyter -v $(current_dir)/..:/analysis $(DOCKER_USERNAME)/openscience-example lab --ip=0.0.0.0 --port=9994 --allow-root
