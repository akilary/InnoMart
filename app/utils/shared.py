from ..models import User, Product


def get_user_by_id(user_id: int) -> User:
    """Возвращает пользователя по ID"""
    user = User.query.get(user_id)
    if not user:
        raise ValueError(f"Пользователь с ID {user_id} не найден")
    return user


def get_product_by_id(product_id: int) -> Product:
    """Возвращает продукт по ID"""
    product = Product.query.get(product_id)
    if not product:
        raise ValueError(f"Товар с ID {product_id} не найден")
    return product
