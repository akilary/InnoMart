from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user, logout_user

from ..utils import delete_user

user_bp = Blueprint("user", __name__, url_prefix="/user")


# Профиль пользователя
@user_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    return render_template("profile.html")


# Удаление аккаунта
@user_bp.route("/delete_account", methods=["POST"])
@login_required
def delete_account():
    try:
        delete_user(current_user.email)
        logout_user()
        flash("Ваш аккаунт удален", "danger")
    except RuntimeError as e:
        flash(str(e), "danger")
    return redirect(url_for("main.home"))
