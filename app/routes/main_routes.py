from flask import Blueprint, render_template, redirect, flash, jsonify, request, url_for
from flask_login import login_required, current_user

from ..utils import (
    get_filtered_paginated_products, get_all_categories, add_to_wishlist, remove_from_wishlist,
    get_cart_items, add_to_cart, remove_from_cart, get_cart_quantity, clear_cart, update_cart_quantity,
    get_order_details, create_order_from_cart
)
from ..utils.shared import get_product_by_id

main_bp = Blueprint("main", __name__, url_prefix="/")


# Основные страницы
@main_bp.route("/")
@main_bp.route("/home")
def home():
    return render_template("pages/home.html")


@main_bp.route("/catalog")
def catalog():
    return render_template("products/catalog.html", categories=get_all_categories())


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
            [render_template("products/product_card.html", product=product) for product in results["data"]]
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
    return render_template("pages/cart.html", user_cart=user_cart)


@main_bp.route("/api/cart/<int:product_id>", methods=["PUT"])
@login_required
def api_add_to_cart(product_id: int):
    try:
        quantity = request.json.get("quantity", 1) if request.is_json else 1
        if request.is_json:
            data = request.get_json()
            print("Получено JSON:", data)
        else:
            print("Не JSON-запрос")
        add_to_cart(current_user.id, product_id, quantity)
        return jsonify({"message": "Товар добавлен в корзину"}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": f"Ошибка сервера: {e}"}), 500


@main_bp.route("/api/cart/<int:product_id>", methods=["PATCH"])
@login_required
def api_update_cart_quantity(product_id: int):
    try:
        if not request.is_json:
            return jsonify({"message": "Требуется JSON"}), 400

        quantity = request.json.get("quantity")
        if not quantity or not isinstance(quantity, int) or quantity < 1:
            return jsonify({"message": "Некорректное количество"}), 400

        update_cart_quantity(current_user.id, product_id, quantity)
        return jsonify({"message": "Количество товара обновлено"}), 200
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


@main_bp.route("/api/cart", methods=["DELETE"])
@login_required
def api_clear_cart():
    try:
        clear_cart(current_user.id)
        return jsonify({"message": "Корзина очищена"}), 200
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
        return render_template("products/product_detail.html", product=get_product_by_id(product_id))
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("main.home"))


# API и страницы для заказов
@main_bp.route("/api/orders", methods=["POST"])
@login_required
def api_create_order():
    try:
        if not current_user.city or not current_user.street or not current_user.postcode:
            return jsonify({
                "message": "Необходимо указать адрес доставки"
            }), 400

        shipping_info = None
        if request.is_json:
            shipping_info = request.json.get("shipping_info")

        order = create_order_from_cart(current_user.id, shipping_info)
        return jsonify({
            "message": "Заказ успешно создан",
            "order_id": order.id
        }), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": f"Ошибка сервера: {e}"}), 500


@main_bp.route("/api/orders/<int:order_id>", methods=["GET"])
@login_required
def api_get_order(order_id: int):
    """Возвращает детали заказа текущего пользователя"""
    try:
        order_details = get_order_details(order_id, current_user.id)

        order_details["created_at"] = order_details["created_at"].isoformat()
        order_details["updated_at"] = order_details["updated_at"].isoformat()

        return jsonify(order_details), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": f"Ошибка сервера: {e}"}), 500
