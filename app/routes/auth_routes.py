from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user

from ..forms import RegistrationForm, LoginForm
from ..utils import create_user, authenticate_user

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = create_user(form.username.data, form.email.data, form.password.data)
            login_user(user)
            flash("Регистрация успешна!", "success")
            return redirect(url_for("main.home"))
        except ValueError as e:
            flash(str(e), "danger")
        except RuntimeError as e:
            flash(str(e), "danger")

    return render_template("register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = authenticate_user(form.username.data, form.password.data)
            login_user(user)
            flash("Вход успешен!", "success")
            return redirect(url_for("main.home"))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template("login.html", form=form)


@auth_bp.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    flash("Вы вышли из системы", "info")
    return redirect(url_for("main.home"))
