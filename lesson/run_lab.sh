#!/bin/sh

docker run -it --rm -p 10000:8888 -e JUPYTER_ENABLE_LAB=yes -e JUPYTER_TOKEN=docker -e MLFLOW_TRACKING_URI=http://localhost:5001 --network mlops-crashcourse --name jupyter -d mlops_notebooks