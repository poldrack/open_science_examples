# Dockerfile for Open science examples

FROM python:3.8-buster

# strategy:
# first build without pegging specific versions
# once everything is running, then rebuild using installed version specified

RUN pip install numpy==1.19.0 \
    pandas==1.0.5 \
    scipy==1.5.0 \
    statsmodels==0.11.1 \
    jupyterlab==2.1.5 \
    seaborn==0.10.1 \
    pytest

WORKDIR /analysis
CMD ["/bin/bash"]
