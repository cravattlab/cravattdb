#!/bin/bash

cd /home/cravattdb/cravatt-ip2/cravattdb
npm install
bower install -F

# start celery daemon
celery -A cravattdb.models.tasks worker --loglevel=info --detach

# install requirements in separate virtual environment
cd /home/cravattdb/cravatt-ip2
virtualenv env
source env/bin/activate
pip install -r requirements.txt

# run the server
python run.py
