#!/bin/sh
# python manage.py makemigrations --name create_user_table
python manage.py migrate
python manage.py start_grpc