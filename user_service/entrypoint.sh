#!/bin/sh
# python manage.py makemigrations --name initiate_tables
python manage.py migrate
python manage.py seed_admin
python manage.py start_grpc