from .shared import get_user_by_id, get_product_by_id
from ..extensions import db
from ..models import Product, Cart


def get_user_cart(user_id: int) -> list[dict[str, any]]:
    """Возвращает корзину пользователя"""
    user = get_user_by_id(user_id)

    cart_items = (
        Cart.query
        .filter_by(user_id=user.id)
        .join(Product)
        .with_entities(
            Product.id,
            Product.name,
            Product.price,
            Product.image_url,
            Cart.quantity
        ).all()
    )

    return [{
        "id": item.id,
        "name": item.name,
        "price": item.price,
        "image_url": item.image_url,
        "quantity": item.quantity,
        "total_price": float(item.price) * item.quantity,
        "date_added": item.date_added
    } for item in cart_items]


def add_to_cart(user_id: int, product_id: int, quantity: int = 1) -> Cart:
    """Добавляет товар в корзину пользователя"""
    user = get_user_by_id(user_id)
    product = get_product_by_id(product_id)

    cart_item = Cart.query.filter_by(user_id=user.id, product_id=product.id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)

    try:
        db.session.add(cart_item)
        db.session.commit()
        return cart_item
    except Exception as e:
        db.session.rollback()
        raise RuntimeError("Ошибка при добавлении в корзину") from e


def remove_from_cart(user_id: int, product_id: int) -> Cart:
    """Удаляет товар из корзины пользователя"""
    user = get_user_by_id(user_id)
    product = get_product_by_id(product_id)

    cart_item = Cart.query.filter_by(user_id=user.id, product_id=product.id).first()
    if not cart_item:
        raise ValueError("Товар не найден в корзине")

    try:
        db.session.delete(cart_item)
        db.session.commit()
        return cart_item
    except Exception as e:
        db.session.rollback()
        raise RuntimeError("Ошибка при удалении из корзины") from e