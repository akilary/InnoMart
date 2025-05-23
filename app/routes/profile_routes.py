from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user, logout_user

from ..utils import delete_user

profile_bp = Blueprint("profile", __name__, url_prefix="/profile")


@profile_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    return render_template("profile.html")


@profile_bp.route("/delete_profile", methods=["POST"])
@login_required
def delete_profile():
    try:
        delete_user(current_user.email)
        logout_user()
        flash("Ваш профиль удален", "danger")
    except RuntimeError as e:
        flash(str(e), "danger")
    return redirect(url_for("main.home"))
