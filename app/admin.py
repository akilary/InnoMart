from flask import Flask, redirect, url_for
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_login import current_user

from .extensions import db
from .models import User, Product, ProductSpec, Cart, Wishlist


class AdminModelView(ModelView):
    """Представление модели в админке"""
    can_view_details = True
    column_display_pk = True
    create_modal = True
    edit_modal = True
    page_size = 20
    can_export = True
    column_export_exclude_list = ["image_url"]

    def is_accessible(self):
        return current_user.is_authenticated and getattr(current_user, "role", "") == "admin"

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login"))


class MyAdminIndexView(AdminIndexView):
    """Главная страница панели администратора"""

    @expose("/")
    def index(self):
        return self.render(
            "admin/dashboard.html",
            user_count=User.query.count(),
            product_count=Product.query.count(),
            wishlist_count=Wishlist.query.count()
        )


class UserAdminView(AdminModelView):
    column_searchable_list = ["username", "email", "phone", "city", "street", "postcode"]
    column_filters = ["role", "city"]
    column_default_sort = ("id", True)

    column_labels = {
        "id": "ID",
        "username": "Имя пользователя",
        "email": "Электронная почта",
        "password": "Пароль",
        "role": "Роль",
        "phone": "Телефон",
        "city": "Город",
        "street": "Улица",
        "postcode": "Почтовый индекс",
        "wishlists": "Списки желаний",
        "carts": "Корзины",
    }

    form_labels = {
        "username": "Имя пользователя",
        "email": "Электронная почта",
        "password": "Пароль",
        "role": "Роль",
        "phone": "Телефон",
        "city": "Город",
        "street": "Улица",
        "postcode": "Почтовый индекс",
    }


class ProductAdminView(AdminModelView):
    column_searchable_list = ["name", "category", "description"]
    column_filters = ["is_new", "is_promotion", "category"]
    column_default_sort = ("id", True)

    column_labels = {
        "id": "ID",
        "name": "Название",
        "description": "Описание",
        "category": "Категория",
        "price": "Цена",
        "stock": "На складе",
        "is_new": "Новинка",
        "is_promotion": "Акция",
        "image_url": "Изображение",
        "wishlisted_by": "В списках желаний",
        "specs": "Спецификации",
        "carted_by": "В корзинах",
    }

    form_labels = {
        "name": "Название",
        "description": "Описание",
        "category": "Категория",
        "price": "Цена",
        "stock": "На складе",
        "is_new": "Новинка",
        "is_promotion": "Акция",
        "image_url": "Изображение",
    }


def init_admin(app: Flask) -> None:
    """Инициализация админки"""
    admin = Admin(name="Inno Mart Admin", template_mode="bootstrap4", index_view=MyAdminIndexView())
    admin.init_app(app)
    models = {
        User: (UserAdminView, "userview", "Пользователи"),
        Product: (ProductAdminView, "productview", "Товары"),
        ProductSpec: (AdminModelView, "specview", "Спецификации"),
        Cart: (AdminModelView, "cartview", "Корзины"),
        Wishlist: (AdminModelView, "wishlistview", "Списки желаний")
    }

    for model, (view_cls, endpoint, name) in models.items():
        admin.add_view(view_cls(model, db.session, endpoint=endpoint, name=name))
    admin.add_link(MenuLink(name="На главную", url="/"))
