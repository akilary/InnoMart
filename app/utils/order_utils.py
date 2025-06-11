from datetime import datetime

from sqlalchemy.orm import joinedload

from .shared import get_user_by_id, get_product_by_id
from .cart_utils import get_cart_items, clear_cart
from ..extensions import db
from ..models import Order, OrderItem, Product


STATUS_CLASS_MAP = {
    "Новый": "pending",
    "Обработан": "processing",
    "Отправлен": "shipped",
    "Доставлен": "delivered",
    "Отменен": "cancelled",
}


def get_user_orders(user_id: int) -> list[dict[str, any]]:
    """Возвращает список заказов пользователя"""
    user = get_user_by_id(user_id)

    orders = (
        Order.query
        .filter_by(user_id=user.id)
        .order_by(Order.created_at.desc())
        .all()
    )

    return [{
        "id": order.id,
        "total_price": float(order.total_price),
        "status": order.status,
        "status_key": STATUS_CLASS_MAP.get(order.status, "pending"),
        "created_at": order.created_at,
        "updated_at": order.updated_at
    } for order in orders]


def get_order_details(order_id: int, user_id: int = None) -> dict[str, any]:
    """Возвращает детали заказа"""
    order = Order.query.get_or_404(order_id)

    if user_id is not None and order.user_id != user_id:
        raise ValueError("Заказ не принадлежит пользователю")

    order_items = (
        OrderItem.query
        .filter_by(order_id=order.id)
        .join(OrderItem.product)
        .options(joinedload(OrderItem.product))
        .all()
    )

    items = [{
        "id": item.product.id,
        "name": item.product.name,
        "price": float(item.price),
        "quantity": item.quantity,
        "total_price": float(item.price) * item.quantity,
        "image_url": item.product.image_url
    } for item in order_items]

    return {
        "id": order.id,
        "user_id": order.user_id,
        "total_price": float(order.total_price),
        "status": order.status,
        "status_key": STATUS_CLASS_MAP.get(order.status, "pending"),
        "shipping_city": order.shipping_city,
        "shipping_street": order.shipping_street,
        "shipping_postcode": order.shipping_postcode,
        "shipping_phone": order.shipping_phone,
        "created_at": order.created_at,
        "updated_at": order.updated_at,
        "items": items
    }


def create_order_from_cart(user_id: int, shipping_info: dict = None) -> Order:
    """Создает заказ на основе корзины пользователя"""
    user = get_user_by_id(user_id)
    cart_items = get_cart_items(user_id)

    if not cart_items:
        raise ValueError("Корзина пуста")

    # Проверка наличия товаров на складе
    for item in cart_items:
        product = get_product_by_id(item["id"])
        if product.stock < item["quantity"]:
            raise ValueError(f"Недостаточно товара '{product.name}' на складе. Доступно: {product.stock}")

    # Создание заказа
    total_price = sum(item["total_price"] for item in cart_items)

    # Добавляем стоимость доставки, если сумма заказа меньше 20000
    shipping_cost = 0.0
    if total_price < 20000:
        shipping_cost = 1500.0

    order = Order(
        user_id=user.id,
        total_price=total_price + shipping_cost,
        status="Новый"
    )

    if shipping_info:
        order.shipping_city = shipping_info.get("city", user.city)
        order.shipping_street = shipping_info.get("street", user.street)
        order.shipping_postcode = shipping_info.get("postcode", user.postcode)
        order.shipping_phone = shipping_info.get("phone", user.phone)
    else:
        order.shipping_city = user.city
        order.shipping_street = user.street
        order.shipping_postcode = user.postcode
        order.shipping_phone = user.phone

    try:
        db.session.add(order)
        db.session.flush()

        # Добавление товаров в заказ
        for item in cart_items:
            product = get_product_by_id(item["id"])
            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=item["quantity"],
                price=product.price
            )
            db.session.add(order_item)

            # Уменьшение количества товара на складе
            product.stock -= item["quantity"]
            db.session.add(product)

        # Очистка корзины
        clear_cart(user_id)

        db.session.commit()
        return order
    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f"Ошибка при создании заказа: {str(e)}") from e


def update_order_status(order_id: int, status: str, user_id: int = None) -> Order:
    """Обновляет статус заказа"""
    order = Order.query.get_or_404(order_id)

    # Проверка, что заказ принадлежит пользователю, если указан user_id
    if user_id is not None and order.user_id != user_id:
        raise ValueError("Заказ не принадлежит пользователю")

    valid_statuses = ["Новый", "Обработан", "Отправлен", "Доставлен", "Отменен"]
    if status not in valid_statuses:
        raise ValueError(f"Недопустимый статус. Допустимые статусы: {', '.join(valid_statuses)}")

    order.status = status
    order.updated_at = datetime.now()

    try:
        db.session.commit()
        return order
    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f"Ошибка при обновлении статуса заказа: {str(e)}") from e


def cancel_order(order_id: int, user_id: int) -> Order:
    """Отменяет заказ и возвращает товары на склад"""
    order = Order.query.get_or_404(order_id)

    # Проверка, что заказ принадлежит пользователю
    if order.user_id != user_id:
        raise ValueError("Заказ не принадлежит пользователю")

    # Проверка, что заказ можно отменить
    if order.status in ["Доставлен", "Отменен"]:
        raise ValueError(f"Невозможно отменить заказ в статусе '{order.status}'")

    try:
        # Возврат товаров на склад
        order_items = OrderItem.query.filter_by(order_id=order.id).all()
        for item in order_items:
            product = Product.query.get(item.product_id)
            product.stock += item.quantity
            db.session.add(product)

        # Обновление статуса заказа
        order.status = "Отменен"
        order.updated_at = datetime.now()

        db.session.commit()
        return order
    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f"Ошибка при отмене заказа: {str(e)}") from e
