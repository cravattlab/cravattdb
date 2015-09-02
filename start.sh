#!/bin/bash

cd /home/cravattdb/cravatt-ip2
npm install
bower install -F
virtualenv env
source env/bin/activate
pip install -r requirements.txt

su rabbitmq -c "rabbitmq-server -detached"
celery -A models.tasks worker --loglevel=info --detach
python index.py