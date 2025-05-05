from ..models import User, Product, Cart


def get_user_cart(user_id: int | None) -> list[dict[str, any]]:
    """Возвращает корзину пользователя"""
    user = User.query.get(user_id)
    if not user:
        raise ValueError(f"Пользователь с ID {user_id} не найден")

    cart_items = (
        Cart.query
        .filter_by(user_id=user_id)
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
        "total_price": float(item.price) * item.quantity
    } for item in cart_items]
