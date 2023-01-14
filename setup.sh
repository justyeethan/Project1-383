#!/bin/bash

# Script to set up the environment easier. You can use this for reference as well

# Create a new environment in python for the project
python3 -m venv venv

# Activate the environment
source venv/bin/activate

# Install the requirements
pip3 install -r requirements.txt

# Run the app
python3 run.py