from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash

from .shared import get_user_by_id
from ..extensions import db
from ..models import User


def create_user(username: str, email: str, password: str) -> User:
    """Создаёт пользователя"""
    if User.query.filter_by(email=email).first():
        raise ValueError("Этот email уже используется.")

    new_user = User(username=username, email=email, password=generate_password_hash(password))

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


def update_user_personal_info(user_id: int, data: dict) -> User:
    """Обновляет личные данные пользователя"""
    user = get_user_by_id(user_id)

    if "email" in data and data["email"] != user.email:
        existing_user = User.query.filter_by(email=data["email"]).first()
        if existing_user:
            raise ValueError("Этот email уже используется другим пользователем")

    print(data)
    if "username" in data and data["username"]:
        user.username = data["username"]
    if "email" in data and data["email"]:
        user.email = data["email"]
    if "phone" in data:
        user.phone = data["phone"]
    
    try:
        db.session.commit()
        return user
    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f"Ошибка обновления данных: {str(e)}") from e


def update_user_address(user_id: int, data: dict) -> User:
    """Обновляет адрес доставки пользователя"""
    user = get_user_by_id(user_id)

    if "city" in data:
        user.city = data["city"]
    if "street" in data:
        user.street = data["street"]
    if "postcode" in data:
        user.postcode = data["postcode"]
    
    try:
        db.session.commit()
        return user
    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f"Ошибка обновления адреса: {str(e)}") from e


def update_user_password(user_id: int, current_password: str, new_password: str) -> User:
    """Обновляет пароль пользователя"""
    user = get_user_by_id(user_id)

    if not check_password_hash(user.password, current_password):
        raise ValueError("Неверный текущий пароль")

    user.password = generate_password_hash(new_password)
    
    try:
        db.session.commit()
        return user
    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f"Ошибка обновления пароля: {str(e)}") from e

