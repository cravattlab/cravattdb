#!/bin/bash

PROJECT_HOME="/home/cravattdb/cravattdb"
# install requirements in virtual environment
cd "${PROJECT_HOME}" || exit
virtualenv --python=/usr/bin/python3.5 env
source env/bin/activate
pip install -r requirements.txt

# start celery daemon
celery -A cravattdb.auto.tasks worker --workdir="${PROJECT_HOME}" --loglevel=info --detach

# get client software
cd "${PROJECT_HOME}/cravattdb/static" || exit
npm install

# run the server
cd "${PROJECT_HOME}" || exit
python run.py
