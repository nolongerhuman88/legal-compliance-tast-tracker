"""Authentication routes."""
from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_user, logout_user, login_required

from app.forms import LoginForm
from app.models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Authenticate user by username and password."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("dashboard.index"))
        flash("Invalid username or password.", "danger")
    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    """Terminate user session."""
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
