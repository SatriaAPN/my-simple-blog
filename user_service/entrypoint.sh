#!/bin/sh
# python manage.py makemigrations --name delete_salt_column_in_user_table
python manage.py migrate
python manage.py start_grpc