#!/bin/bash

cd /home/cravattdb/cravatt-ip2
npm install
bower install -F
virtualenv env
source env/bin/activate
pip install -r requirements.txt

tail -f .gitignore