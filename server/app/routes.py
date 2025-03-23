from flask import Blueprint, redirect, url_for, jsonify, render_template, request
import requests
from flask_dance.contrib.google import google
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app.oauth import google_bp
from app import login_manager   

auth_bp = Blueprint("auth", __name__)
auth_bp.register_blueprint(google_bp, url_prefix="/login")

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@auth_bp.route("/google")
def google_login():
    if not google.authorized:
        return redirect(url_for("auth.google.login"))
    resp = google.get("/oauth2/v1/userinfo")
    if resp.ok:
        user_data = resp.json()
        print("Google Response:", user_data)  

        user_id = user_data["id"]
        user_name = user_data.get("name", "Unknown")
        user_email = user_data.get("email", f"{user_id}@google.com") 
        profile_pic = user_data.get("picture", "")
        user = User.create_or_update(user_id, user_name, user_email, profile_pic)
        login_user(user)
        return redirect(url_for("auth.profile"))

    return "Google authentication failed!", 401

@auth_bp.route("/profile")
@login_required  
def profile():
    return jsonify({
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email
    })

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("google.login"))

@auth_bp.route("/")
@login_required 
def index():
    """Root route that requires login to access."""
    user_data = {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "isAuthenticated": True,
        "profile_pic": current_user.profile_pic
    }
    return render_template("index.html", current_user=user_data)

@auth_bp.route('/chat', methods=['POST'])
@login_required
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    url = "http://127.0.0.1:8000/api/v1/chat"
    
    try:
        # Forward the request to your API
        api_response = requests.post(
            url, 
            json={
                "message": user_message,
                "user_id": current_user.id,
                "thread_id": "123"
            }
        )
        return api_response.json()
    except Exception as e:
        # Handle errors
        print(f"Error calling API: {str(e)}")
        return jsonify({
            'message': "I'm sorry, I couldn't process your request. Please try again later.",
            'Thinking': "<Thinking>Error connecting to API server</think>"
        })
