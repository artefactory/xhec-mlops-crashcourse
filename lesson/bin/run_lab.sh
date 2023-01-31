#!/bin/sh

docker run -it --rm --user root -p 10000:8888 -p 8000:8000 -p 4200:4200 -e JUPYTER_ENABLE_LAB=yes -e JUPYTER_TOKEN=docker -e MLFLOW_TRACKING_URI=http://mlflow:5001 --network mlops-crashcourse --name jupyter -d mlops_notebooks