from flaskwebgui import FlaskUI
from first_project.wsgi import application


FlaskUI(application).run(host='127.0.0.1',port="80")