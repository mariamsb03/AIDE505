from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-secret-key-in-production")

# FastAPI backend URL
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")

@app.route("/")
def index():
    if "token" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if not username or not password:
            flash("Username and password are required", "error")
            return render_template("login.html")
        
        try:
            # Call FastAPI login endpoint
            response = requests.post(
                f"{FASTAPI_URL}/login",
                json={"username": username, "password": password},
                timeout=5
            )
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    session["token"] = data["access_token"]
                    session["username"] = username
                    flash("Login successful!", "success")
                    return redirect(url_for("dashboard"))
                except ValueError:
                    flash("Invalid response from server", "error")
            else:
                try:
                    error_data = response.json()
                    error_message = error_data.get("detail", "Login failed")
                except ValueError:
                    error_message = f"Login failed with status {response.status_code}"
                flash(error_message, "error")
        except requests.exceptions.Timeout:
            flash("Connection timeout. Please check if the backend server is running.", "error")
        except requests.exceptions.ConnectionError:
            flash("Cannot connect to backend server. Please ensure the FastAPI server is running.", "error")
        except requests.exceptions.RequestException as e:
            flash(f"Connection error: {str(e)}", "error")
        except Exception as e:
            flash(f"Unexpected error: {str(e)}", "error")
    
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        
        if not username or not email or not password:
            flash("All fields are required", "error")
            return render_template("register.html")
        
        try:
            # Call FastAPI register endpoint
            response = requests.post(
                f"{FASTAPI_URL}/register",
                json={"username": username, "email": email, "password": password},
                timeout=5
            )
            
            if response.status_code == 200:
                flash("Registration successful! Please login.", "success")
                return redirect(url_for("login"))
            else:
                try:
                    error_data = response.json()
                    error_message = error_data.get("detail", "Registration failed")
                except ValueError:
                    error_message = f"Registration failed with status {response.status_code}"
                flash(error_message, "error")
        except requests.exceptions.Timeout:
            flash("Connection timeout. Please check if the backend server is running.", "error")
        except requests.exceptions.ConnectionError:
            flash("Cannot connect to backend server. Please ensure the FastAPI server is running.", "error")
        except requests.exceptions.RequestException as e:
            flash(f"Connection error: {str(e)}", "error")
        except Exception as e:
            flash(f"Unexpected error: {str(e)}", "error")
    
    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    if "token" not in session:
        flash("Please login to access the dashboard", "error")
        return redirect(url_for("login"))
    
    username = session.get("username", "User")
    return render_template("dashboard.html", username=username)

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out", "info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

