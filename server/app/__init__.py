from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from app.config import Config

login_manager = LoginManager()
mongo = PyMongo()

def create_app():
    try:
        app = Flask(__name__)
        app.config.from_object(Config)
        

        mongo.init_app(app)
        login_manager.init_app(app)
        
        login_manager.login_view = "auth.google_login"


        from app.routes import auth_bp
        app.register_blueprint(auth_bp)

        return app
    except Exception as e:
        print(f"Error during app creation: {e}")  
        return None
