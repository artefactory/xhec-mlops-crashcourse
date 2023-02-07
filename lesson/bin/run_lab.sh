#!/bin/sh

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
SCRIPTPATH=$(builtin cd $SCRIPTPATH/../../mlflow_server; pwd)

docker run -it --rm --user root -p 10000:8888 -p 8000:8000 -p 4200:4200 -p 5002:5002 -v ${SCRIPTPATH}/local:/mlflow -e JUPYTER_ENABLE_LAB=yes -e JUPYTER_TOKEN=docker --network mlops-crashcourse --name jupyter -d mlops_notebooks
