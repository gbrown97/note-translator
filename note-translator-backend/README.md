# note-translator
Repository for Note Translator code and documents
Test

HOW TO RUN

TO RUN IN VIRT ENV (FOR DEV ENV)

python3 -m venv env
source env/bin/activate

DEPENDENCIES

$ pip install Flask \
    Flask-SQLAlchemy \
    Flask-RESTful \
    flask-marshmallow

TO SETUP DATABASE (ONLY ONCE)
(env) $ python3
>>> from application import db,app
>>> app.app_context().push()
>>> db.create_all()
>>> exit()

HOW TO RUN

Run the following command in your terminal or command prompt to run the application

python3 application.py

Navigate to "http://localhost:5000/" in a web browser.