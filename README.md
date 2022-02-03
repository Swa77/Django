# Django
# Installing Required applications - 
Python (3.6, 3.7, 3.8, 3.9, 3.10)
Django (2.2, 3.0, 3.1, 3.2, 4.0)
# Installation
Install using pip...

pip install djangorestframework

Add 'rest_framework' to your INSTALLED_APPS setting.

INSTALLED_APPS = [
    ...
    'rest_framework',
]

## Example
pip install django

pip install djangorestframework

django-admin startproject example .

./manage.py migrate

./manage.py createsuperuser

## 3. Installing Postman 
Provide Url which edition installed 

## 4. Installing PyCharm and Basic setup (INCLUDE GIT Pull/init/clone)

git pull https://github.com/Swa77/Django.git 

# How to Config Project in Pycharm

## 1. Creating Virtual Environment
virtualenv django_project

## 2. Installing Dependencies - 
pip install -r requirements.txt 

## 3. Getting into Virtualenv (django_project) - 
activate django_project

## 4. Migrations for Model - 
python manage.py makemigrations
python manage.py migrate 
python manage.py check 

## 5. Run Server in Local 
python manage.py runserver
