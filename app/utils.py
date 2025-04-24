from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db
from .models import User, Product, Wishlist


# ============================================================
# Утилиты для работы с товарами
# ============================================================

def get_filtered_paginated_products(
        page: int,
        per_page: int,
        price_min: float | None,
        price_max: float | None,
        categories: list[str] | None,
        sort_by: str | None,
        user_id: int | None,
) -> dict[str, any]:
    """Возвращает товары с пагинацией и фильтрацией"""
    query = Product.query

    if price_min is not None:
        query = query.filter(Product.price >= price_min)
    if price_max is not None:
        query = query.filter(Product.price <= price_max)
    if categories:
        query = query.filter(Product.category.in_(categories))

    sort_mapping = {
        "price_asc": Product.price.asc(),
        "price_desc": Product.price.desc(),
        "new": Product.query.all(),
        "discount": Product.query.all()
    }

    if sort_by in sort_mapping and sort_mapping[sort_by] is not None:
        query = query.order_by(sort_mapping[sort_by])

    wishlist_ids = set()
    if user_id:
        wishlist_ids = {
            w.product_id for w in Wishlist.query.filter_by(user_id=user_id).with_entities(Wishlist.product_id).all()
        }

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    products = [{
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "category": product.category,
        "image_url": product.image_url,
        "in_wishlist": product.id in wishlist_ids,
    } for product in pagination.items]

    return {
        "data": products,
        "page": page,
        "per_page": per_page,
        "total_pages": pagination.pages,
        "total_items": pagination.total,
    }

def get_product(product_id: int) -> Product:
    """Возвращает информацию о продукте"""
    product = Product.query.get(product_id)
    if not product:
        raise ValueError(f"Продукт c ID {product_id} не найден")

    return product

# ============================================================
#                   User Utilities
# ============================================================

def create_user(username: str, email: str, password: str) -> User:
    """Создаёт пользователя"""
    if User.query.filter_by(email=email).first():
        raise ValueError("Этот email уже используется.")

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except Exception as e:
        db.session.rollback()
        raise RuntimeError("Ошибка регистрации, попробуйте снова!") from e


def authenticate_user(login: str, password: str) -> User:
    """Проверяет логин и пароль"""
    user = User.query.filter(or_(User.email == login, User.username == login)).first()

    if not user or not check_password_hash(user.password, password):
        raise ValueError("Неверный логин или пароль!")
    return user


def update_user(user_id: str, user_data: dict[str, any]) -> None:
    """Обновляет данные пользователя"""
    user = User.query.get(user_id)
    if not user:
        raise ValueError(f"Пользователь с ID {user_id} не найден")

    if "current_password" in user_data and user_data["current_password"]:
        if not check_password_hash(user.password, user_data["current_password"]):
            raise ValueError("Неверный текущий пароль")

    for field_name, field_value in user_data.items():
        if field_name == "current_password":
            continue
        if field_value is not None:
            if field_name == "new_password" and field_value:
                user.password = generate_password_hash(field_value)
            else:
                setattr(user, field_name, field_value)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise RuntimeError("Ошибка обновления профиля") from e


def delete_user(email: str) -> None:
    """Удаляет пользователя по email"""
    user = User.query.filter_by(email=email).first()

    if not user:
        raise ValueError(f"Пользователь с email {email} не найден.")

    try:
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise RuntimeError("Ошибка удаления пользователя.") from e


# ============================================================
#                 Wishlist Utilities
# ============================================================

def get_user_wishlist(user_id: int) -> list[dict[str, any]]:
    """Возвращает избранное пользователя"""
    user = User.query.get(user_id)
    if not user:
        raise ValueError(f"Пользователь с ID {user_id} не найден")

    wishlist_items = (Wishlist.query
                      .filter_by(user_id=user_id)
                      .join(Product)
                      .with_entities(Product.id, Product.name)
                      .all())

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
