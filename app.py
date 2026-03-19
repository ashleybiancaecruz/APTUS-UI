from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "replace-with-a-secure-random-key"

# Simple in-memory user store for demo. In production use a database.
users = {
    "demo@aptus.app": {
        "name": "Demo User",
        "password_hash": generate_password_hash("Password123")
    }
}

@app.route("/")
def landing():
    if session.get("user_email"):
        return redirect(url_for("dashboard"))
    return render_template("landing.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            flash("Please fill in all fields.", "error")
            return redirect(url_for("register"))

        if email in users:
            flash("Email already registered. Please log in.", "error")
            return redirect(url_for("login"))

        users[email] = {
            "name": name,
            "password_hash": generate_password_hash(password)
        }
        flash("Registration complete. Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = users.get(email)
        if user and check_password_hash(user["password_hash"], password):
            session["user_email"] = email
            session["user_name"] = user.get("name", "User")
            flash("Logged in successfully.", "success")
            return redirect(url_for("dashboard"))

        flash("Invalid email or password.", "error")
        return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if not session.get("user_email"):
        flash("Please log in first.", "error")
        return redirect(url_for("login"))
    return render_template("dashboard.html", user_name=session.get("user_name"))

@app.route("/logout")
def logout():
    session.clear()
    flash("You have logged out.", "success")
    return redirect(url_for("landing"))

if __name__ == "__main__":
    app.run(debug=True)
