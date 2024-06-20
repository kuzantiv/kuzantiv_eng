#!/bin/bash

# Ensure Python and pip are installed
if ! command -v python3.12 &> /dev/null
then
    echo "Python 3.12 could not be found"
    exit 1
fi

# create a virtual environment named 'venv' if it doesn't already exist
python3.12 -m venv venv

# activate the virtual environment
source venv/bin/activate

if ! command -v pip &> /dev/null
then
    echo "pip could not be found"
    exit 1
fi

# Install dependencies
pip install -r requirements.txt

# Run Django management commands
python3.12 manage.py collectstatic --noinput
python3.12 manage.py migrate
