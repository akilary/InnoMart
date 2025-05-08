from .shared import get_user_by_id, get_product_by_id
from ..extensions import db
from ..models import Product, Wishlist


def get_user_wishlist(user_id: int) -> list[dict[str, any]]:
    """Возвращает избранное пользователя"""
    user = get_user_by_id(user_id)

    wishlist_items = (
        Wishlist.query
        .filter_by(user_id=user.id)
        .join(Product)
        .with_entities(Product.id, Product.name)
        .all()
    )
    return [{
        "id": item.id,
        "name": item.name,
        "date_added": item.date_added
    } for item in wishlist_items]


def add_to_wishlist(user_id: int, product_id: int) -> Wishlist:
    """Добавляет товар в избранное"""
    user = get_user_by_id(user_id)
    product = get_product_by_id(product_id)

    existing_item = Wishlist.query.filter_by(user_id=user.id, product_id=product.id).first()
    if existing_item:
        raise ValueError("Товар уже добавлен в избранное")

    wishlist_item = Wishlist(user_id=user.id, product_id=product.id)
    try:
        db.session.add(wishlist_item)
        db.session.commit()
        return wishlist_item
    except Exception as e:
        db.session.rollback()
        raise RuntimeError("Ошибка при добавлении в избранное") from e


def remove_from_wishlist(user_id: int, product_id: int) -> Wishlist:
    """Удаляет товар из избранного"""
    user = get_user_by_id(user_id)
    product = get_product_by_id(product_id)

    wishlist_item = Wishlist.query.filter_by(user_id=user.id, product_id=product.id).first()
    if not wishlist_item:
        raise ValueError("Товар не найден в избранном")
    try:
        db.session.delete(wishlist_item)
        db.session.commit()
        return wishlist_item
    except Exception as e:
        db.session.rollback()
        raise RuntimeError("Ошибка при удалении из избранного") from e
