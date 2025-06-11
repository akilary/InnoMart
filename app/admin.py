from flask import Flask, redirect, url_for
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_login import current_user
from markupsafe import Markup

from .extensions import db
from .models import User, Product, ProductSpec, Cart, Wishlist, Order, OrderItem, ProductCategory, ProductGallery


def _image_formatter(view, context, model, name):
    if model.image_url:
        return Markup(f'<img src="{model.image_url}" style="max-height: 50px;">')
    return ""


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
            wishlist_count=Wishlist.query.count(),
            order_count=Order.query.count(),
            category_count=ProductCategory.query.count()
        )


class UserAdminView(AdminModelView):
    """Представление модели User в админке"""
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
    """Представление модели Product в админке"""
    column_searchable_list = ["name", "category.name", "description"]
    column_filters = ["is_new", "is_promotion", "category.name", "stock"]
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

    column_formatters = {"image_url": _image_formatter}

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


class OrderAdminView(AdminModelView):
    """Представление модели Order в админке"""
    column_list = ["id", "user", "total_price", "status", "created_at", "updated_at"]
    column_filters = ["status", "created_at"]
    column_searchable_list = ["user.username", "shipping_city", "shipping_street"]
    column_labels = {
        "id": "ID",
        "user": "Пользователь",
        "total_price": "Сумма",
        "status": "Статус",
        "shipping_city": "Город",
        "shipping_street": "Улица",
        "shipping_postcode": "Почтовый индекс",
        "shipping_phone": "Телефон",
        "created_at": "Создан",
        "updated_at": "Обновлён",
        "items": "Товары в заказе"
    }


class CategoryAdminView(AdminModelView):
    """Представление модели Category в админке"""
    column_list = ["id", "name", "slug", "icon"]
    column_searchable_list = ["name", "slug"]
    form_labels = {
        "name": "Название категории",
        "slug": "Слаг (URL)",
        "icon": "Иконка (URL)",
    }

class OrderItemAdminView(AdminModelView):
    """Представление модели OrderItem в админке"""
    column_list = ["order_id", "product", "quantity", "price"]
    column_labels = {
        "order_id": "ID Заказа",
        "product": "Товар",
        "quantity": "Количество",
        "price": "Цена",
    }

class ProductGalleryAdminView(AdminModelView):
    """Представление модели ProductGallery в админке"""
    column_list = ["id", "product", "image_url"]
    column_formatters = {"image_url": _image_formatter}
    column_labels = {
        "id": "ID",
        "product": "Товар",
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
        Wishlist: (AdminModelView, "wishlistview", "Списки желаний"),
        Order: (OrderAdminView, "orderview", "Заказы"),
        OrderItem: (OrderItemAdminView, "orderitemview", "Товары в заказах"),
        ProductCategory: (CategoryAdminView, "categoryview", "Категории"),
        ProductGallery: (ProductGalleryAdminView, "galleryview", "Галерея товаров"),
    }

    for model, (view_cls, endpoint, name) in models.items():
        admin.add_view(view_cls(model, db.session, endpoint=endpoint, name=name))
    admin.add_link(MenuLink(name="На главную", url="/"))
