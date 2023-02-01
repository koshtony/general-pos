from flaskwebgui import FlaskUI
from first_project.wsgi import application


FlaskUI(application).run()