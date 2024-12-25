#!/bin/sh
# python manage.py makemigrations --name blog_table_update_content_len_limit_to_12000
python manage.py migrate
python manage.py start_grpc