from flask import Blueprint, render_template, redirect, flash, jsonify, request
from flask_login import login_required, current_user

from ..utils import (
    get_filtered_paginated_products, add_to_wishlist, remove_from_wishlist, get_cart_items, add_to_cart,
    remove_from_cart, get_cart_quantity
)
from ..utils.shared import get_product_by_id

main_bp = Blueprint("main", __name__, url_prefix="/")


# Основные страницы
@main_bp.route("/")
@main_bp.route("/home")
def home():
    return render_template("home.html")


@main_bp.route("/catalog")
def catalog():
    return render_template("catalog.html")


# API для продуктов
@main_bp.route("/api/products", methods=["GET"])
def api_get_products():
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)
        price_min = request.args.get("price_min", type=int)
        price_max = request.args.get("price_max", type=int)
        categories = request.args.getlist("categories")
        sort_by = request.args.get("sort_by")

        results = get_filtered_paginated_products(
            user_id=current_user.id if current_user.is_authenticated else -1,
            page=page,
            per_page=per_page,
            categories=categories,
            price_min=price_min,
            price_max=price_max,
            sort_by=sort_by
        )
        rendered_html = "".join(
            [render_template("product_card.html", product=product) for product in results["data"]]
        )
        return jsonify({
            "html": rendered_html,
            "page": results["page"],
            "total_pages": results["total_pages"],
            "total_items": results["total_items"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Страница и API для корзины
@main_bp.route("/cart")
@login_required
def cart():
    user_cart = get_cart_items(current_user.id)
    return render_template("cart.html", user_cart=user_cart)


@main_bp.route("/api/cart/<int:product_id>", methods=["PUT"])
@login_required
def api_add_to_cart(product_id: int):
    try:
        add_to_cart(current_user.id, product_id)
        return jsonify({"message": "Товар добавлен в корзину"}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": f"Ошибка сервера: {e}"}), 500


@main_bp.route("/api/cart/<int:product_id>", methods=["DELETE"])
@login_required
def api_remove_from_cart(product_id: int):
    try:
        remove_from_cart(current_user.id, product_id)
        return jsonify({"message": "Товар удалён из корзины"}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": f"Ошибка сервера: {e}"}), 500


@main_bp.route("/api/cart/quantity", methods=["GET"])
@login_required
def api_get_cart_quantity():
    try:
        return jsonify({"message": "Количество товаров в корзине", "quantity": get_cart_quantity(current_user.id)}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": f"Ошибка сервера: {e}"}), 500


# API для избранного
@main_bp.route("/api/wishlist/<int:product_id>", methods=["PUT"])
@login_required
def api_add_to_wishlist(product_id: int):
    try:
        add_to_wishlist(current_user.id, product_id)
        return jsonify({"message": "Товар добавлен в избранное"}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": f"Ошибка сервера: {e}"}), 500


@main_bp.route("/api/wishlist/<int:product_id>", methods=["DELETE"])
@login_required
def api_remove_from_wishlist(product_id: int):
    try:
        remove_from_wishlist(current_user.id, product_id)
        return jsonify({"message": "Товар удалён из избранного"}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": f"Ошибка сервера: {e}"}), 500


# Страница деталей продукта
@main_bp.route("/product/<int:product_id>", methods=["GET"])
def product_details(product_id: int):
    try:
        return render_template("product_detail.html", product=get_product_by_id(product_id))
    except ValueError as e:
        flash(str(e), "danger")
        return redirect("home")
