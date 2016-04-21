#!/bin/bash

# install requirements in virtual environment
cd /home/cravattdb/cravattdb
virtualenv env
source env/bin/activate
pip install -r requirements.txt

# start celery daemon
celery -A cravattdb.models.tasks worker --loglevel=info --detach

# get client software
cd /home/cravattdb/cravattdb/cravattdb
npm install
bower install -F

# run the server
cd /home/cravattdb/cravattdb
python run.py
