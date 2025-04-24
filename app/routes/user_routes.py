from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user, logout_user

from ..forms import UpdateProfileForm
from ..utils import get_user_wishlist, update_user, delete_user

user_bp = Blueprint("user", __name__, url_prefix="/user")


@user_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        try:
            update_user(current_user.id, form.data)
            flash("Данные для пользователя обновлены", "success")
        except ValueError as e:
            flash(str(e), "danger")
        except RuntimeError as e:
            flash(str(e), "danger")
    wishlist_data = get_user_wishlist(current_user.id)
    return render_template("profile.html", form=form, wishlist_data=wishlist_data)


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
