#!/bin/sh
# python manage.py makemigrations --name initiate_tables
python manage.py migrate
python manage.py start_grpc