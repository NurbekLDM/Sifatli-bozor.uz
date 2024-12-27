#!/bin/bash

black .

sleep 1

pip freeze > requirements.txt

sleep 1

python manage.py makemigrations

sleep 1

python manage.py migrate

sleep 1

python manage.py test

sleep 1

python manage.py runserver

