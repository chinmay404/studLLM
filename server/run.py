# from flask import Flask, redirect, url_for, session, jsonify
# from flask_dance.contrib.google import make_google_blueprint, google
# from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
# import os
# from utils import get_google_blueprint


# app = Flask(__name__)
# app.secret_key = "edf82b22-06ba-46a3-9191-9a9437571659"
# # OAuth Config
# os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Allow HTTP for local testing
# google_bp = get_google_blueprint()
# app.register_blueprint(google_bp, url_prefix="/login")


# # Flask-Login Setup
# login_manager = LoginManager()
# login_manager.init_app(app)


from app import create_app
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
