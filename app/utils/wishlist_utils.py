from .shared import get_user_by_id, get_product_by_id
from ..extensions import db
from ..models import Product, Wishlist


def get_wishlist_count(user_id: int) -> int:
    """Возвращает количество товаров в избранном пользователя"""
    user = get_user_by_id(user_id)
    return Wishlist.query.filter_by(user_id=user.id).count()


def get_wishlist_items(user_id: int) -> list[dict[str, any]]:
    """Возвращает избранное пользователя"""
    user = get_user_by_id(user_id)

    wishlist_items = (
        Wishlist.query
        .filter_by(user_id=user.id)
        .join(Product)
        .with_entities(
            Product.id,
            Product.name,
            Product.price,
            Product.image_url,
            Product.category,
            Wishlist.date_added
        )
        .all()
    )

    return [{
        "id": item.id,
        "name": item.name,
        "price": item.price,
        "image_url": item.image_url,
        "category": item.category,
        "date_added": item.date_added
    } for item in wishlist_items]


def add_to_wishlist(user_id: int, product_id: int) -> bool:
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
        return True
    except Exception as e:
        db.session.rollback()
        raise RuntimeError("Ошибка при добавлении в избранное") from e


def remove_from_wishlist(user_id: int, product_id: int) -> bool:
    """Удаляет товар из избранного"""
    user = get_user_by_id(user_id)
    product = get_product_by_id(product_id)

    wishlist_item = Wishlist.query.filter_by(user_id=user.id, product_id=product.id).first()
    if not wishlist_item:
        raise ValueError("Товар не найден в избранном")
    try:
        db.session.delete(wishlist_item)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise RuntimeError("Ошибка при удалении из избранного") from e


def clear_wishlist(user_id: int) -> bool:
    """Очищает все избранное пользователя"""
    user = get_user_by_id(user_id)

    try:
        Wishlist.query.filter_by(user_id=user.id).delete()
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise RuntimeError("Ошибка при очистке избранного") from e
