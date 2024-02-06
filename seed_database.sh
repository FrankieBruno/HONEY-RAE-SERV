#!/bin/bash

rm db.sqlite3
rm -rf ./repairsapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations repairsapi
python3 manage.py migrate repairsapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata customers
python3 manage.py loaddata employees
python3 manage.py loaddata tickets