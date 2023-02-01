#!/bin/bash

echo "Initialization: Installing requirements"
python -V
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
