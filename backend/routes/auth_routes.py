from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from backend.services.auth_service import authenticate_user, create_user


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_email") and session.get("user_id"):
        return redirect(url_for("debug.index"))
    if session.get("user_email") and not session.get("user_id"):
        session.clear()

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = authenticate_user(email, password)

        if user:
            session.clear()
            session["user_email"] = user["email"]
            session["user_name"] = user["name"]
            session["user_id"] = user["id"]
            session.permanent = True
            flash("Welcome back. You are now logged in.", "success")
            return redirect(url_for("debug.index"))

        flash("Invalid email or password. Please try again.", "error")
        return render_template("login.html", form_email=email)

    return render_template("login.html")


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if session.get("user_email") and session.get("user_id"):
        return redirect(url_for("debug.index"))
    if session.get("user_email") and not session.get("user_id"):
        session.clear()

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if password != confirm_password:
            flash("Passwords do not match. Please enter them again.", "error")
            return render_template("signup.html", form_name=name, form_email=email)

        ok, message = create_user(name, email, password)
        if not ok:
            flash(message, "error")
            return render_template("signup.html", form_name=name, form_email=email)

        flash("Account created successfully. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("signup.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))
