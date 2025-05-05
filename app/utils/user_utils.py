from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash

from ..extensions import db
from ..models import User


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
