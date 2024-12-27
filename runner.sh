#!/bin/bash

black .

pip freeze > requirements.txt

python manage.py makemigrations

python manage.py migrate

python manage.py test

python manage.py runserver

