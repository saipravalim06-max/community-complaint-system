from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models import User, Role
from .forms import CitizenSignupForm, CitizenLoginForm
from werkzeug.security import check_password_hash

auth_bp = Blueprint("auth", __name__, template_folder="../templates")

# ---------------------------
# CITIZEN SIGNUP
# ---------------------------
@auth_bp.route("/signup/citizen", methods=["GET", "POST"])
def signup_citizen():
    if current_user.is_authenticated:
        return redirect(url_for("citizen.dashboard"))

    form = CitizenSignupForm()
    if form.validate_on_submit():
        role = Role.query.filter_by(name="citizen").first()
        user = User(
            username=form.username.data,
            email=form.email.data,
            role_id=role.id
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("✅ Account created successfully! Please log in.", "success")
        return redirect(url_for("auth.login_citizen"))
    return render_template("signup_citizen.html", form=form)

# ---------------------------
# CITIZEN LOGIN
# ---------------------------
@auth_bp.route("/login/citizen", methods=["GET", "POST"])
def login_citizen():
    if current_user.is_authenticated:
        return redirect(url_for("citizen.dashboard"))

    form = CitizenLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        citizen_role = Role.query.filter_by(name="citizen").first()
        if user and user.role_id == citizen_role.id and user.check_password(form.password.data):
            login_user(user)
            flash("Welcome Citizen!", "success")
            return redirect(url_for("citizen.dashboard"))
        else:
            flash("Invalid credentials for Citizen.", "danger")
    return render_template("login_citizen.html", form=form)

# ---------------------------
# ADMIN LOGIN
# ---------------------------
@auth_bp.route("/login/admin", methods=["GET", "POST"])
def login_admin():
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))

    form = CitizenLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        admin_role = Role.query.filter_by(name="admin").first()
        if user and user.role_id == admin_role.id and user.check_password(form.password.data):
            login_user(user)
            flash("Welcome Admin!", "success")
            return redirect(url_for("admin.dashboard"))
        else:
            flash("Invalid credentials for Admin.", "danger")
    return render_template("login_admin.html", form=form)

# ---------------------------
# SUPER ADMIN LOGIN
# ---------------------------
@auth_bp.route("/login/superadmin", methods=["GET", "POST"])
def login_superadmin():
    if current_user.is_authenticated:
        return redirect(url_for("superadmin.dashboard"))

    form = CitizenLoginForm()  # we’re reusing the same login form
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        super_role = Role.query.filter_by(name="superadmin").first()
        if user and user.role_id == super_role.id and user.check_password(form.password.data):
            login_user(user)
            flash("Welcome Super Admin!", "success")
            return redirect(url_for("superadmin.dashboard"))
        else:
            flash("Invalid credentials for Super Admin.", "danger")
    return render_template("login_superadmin.html", form=form)


# ---------------------------
# LOGOUT
# ---------------------------
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))
