# real_time_chat
web application for create chat platform between people

this project has two part : 1- server that emplimented with django 2- client that implimented with angular

## backend
this server is created with channel and django with redis 

for runing this part first install requirements libs:
pip install -r requirements.txt

then you most create a .env that store your informations data:
in backend/.env:
SECRET_KEY=
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

now its time to run the project:
python manage.py runserver

## frontend
to run this part just run npm install and then ng serve

