#!/bin/bash

# install requirements in virtual environment
cd /home/cravattdb/cravattdb
virtualenv --python=/usr/bin/python3.5 env
source env/bin/activate
pip install -r requirements.txt

# start celery daemon
celery -A cravattdb.auto.tasks worker --loglevel=info --detach

# get client software
cd /home/cravattdb/cravattdb/cravattdb/static
npm install
bower install -F

# run the server
cd /home/cravattdb/cravattdb
python run.py
