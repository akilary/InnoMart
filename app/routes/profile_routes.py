from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, request
from flask_login import login_required, current_user, logout_user

from ..utils import (
    delete_user, get_wishlist_items, get_user_orders,
    update_user_personal_info, update_user_address
)
from ..forms import AddressForm, PersonalForm

profile_bp = Blueprint("profile", __name__, url_prefix="/profile")


@profile_bp.route("/", methods=["GET", "POST"])
@login_required
def profile():
    address_form = AddressForm()
    personal_form = PersonalForm()

    if address_form.validate_on_submit():
        try:
            update_user_address(current_user.id, address_form.data)
            return redirect(url_for("profile.profile"))
        except ValueError as e:
            return jsonify({"message": str(e)}), 400
        except Exception as e:
            return jsonify({"message": f"Ошибка сервера: {e}"}), 500

    if personal_form.validate_on_submit():
        try:
            update_user_personal_info(current_user.id, personal_form.data)
            return redirect(url_for("profile.profile"))
        except ValueError as e:
            return jsonify({"message": str(e)}), 400
        except Exception as e:
            return jsonify({"message": f"Ошибка сервера: {e}"}), 500

    return render_template(
        "user/profile.html", wishlist_items=get_wishlist_items(current_user.id),
        orders=get_user_orders(current_user.id), address_form=address_form, personal_form=personal_form
    )


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
