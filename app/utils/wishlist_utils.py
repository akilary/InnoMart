from ..extensions import db
from ..models import User, Product, Wishlist


def get_user_wishlist(user_id: int) -> list[dict[str, any]]:
    """Возвращает избранное пользователя"""
    user = User.query.get(user_id)
    if not user:
        raise ValueError(f"Пользователь с ID {user_id} не найден")

    wishlist_items = (
        Wishlist.query
        .filter_by(user_id=user_id)
        .join(Product)
        .with_entities(Product.id, Product.name)
        .all()
    )
    return [{"id": item.id, "name": item.name} for item in wishlist_items]


def add_to_wishlist(user_id: int, product_id: int) -> Wishlist:
    """Добавляет товар в избранное"""
    user = User.query.get(user_id)
    if not user:
        raise ValueError(f"Пользователь с ID {user_id} не найден")

    product = Product.query.get(product_id)
    if not product:
        raise ValueError(f"Продукт c ID {product_id} не найден")

    existing_item = Wishlist.query.filter_by(user_id=user_id, product_id=product_id).first()
    if existing_item:
        raise ValueError("Товар уже добавлен в избранное")

    new_item = Wishlist(user_id=user_id, product_id=product_id)
    try:
        db.session.add(new_item)
        db.session.commit()
        return new_item
    except Exception as e:
        db.session.rollback()
        raise RuntimeError("Ошибка при добавлении в избранное") from e


def remove_from_wishlist(user_id: int, product_id: int) -> Wishlist:
    """Удаляет товар из избранного"""
    item = Wishlist.query.filter_by(user_id=user_id, product_id=product_id).first()
    if not item:
        raise ValueError("Товар не найден в избранном")
    try:
        db.session.delete(item)
        db.session.commit()
        return item
    except Exception as e:
        db.session.rollback()
        raise RuntimeError("Ошибка при удалении из избранного") from e
