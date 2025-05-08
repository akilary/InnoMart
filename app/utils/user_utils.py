from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash

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
