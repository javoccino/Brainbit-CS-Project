#makes the parts of whole folder a python package
from flask import Flask

def create_app():
    app = Flask(__name__) #initializing Flask
    app.config['SECRET_KEY'] = 'orkgkerokogekmdk'

    from .views import views #importing views blueprint from views.py
    from .auth import auth #importing auth blueprint from auth.py

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    return app