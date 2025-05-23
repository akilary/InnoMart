from datetime import datetime

from flask_login import UserMixin

from .extensions import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """Модель пользователя"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(50), nullable=False, default="user")

    phone = db.Column(db.String(20), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    street = db.Column(db.String(200), nullable=True)
    postcode = db.Column(db.String(9), nullable=True)

    wishlists = db.relationship("Wishlist", back_populates="user", cascade="all, delete-orphan", lazy="dynamic")
    carts = db.relationship("Cart", back_populates="user", cascade="all, delete-orphan", lazy="dynamic")

    def __repr__(self):
        return f"<User {self.username}>"


class Product(db.Model):
    """Модель товара"""
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

    is_new = db.Column(db.Boolean, nullable=False, default=False)
    is_promotion = db.Column(db.Boolean, nullable=False, default=False)

    image_url = db.Column(db.String(255), nullable=True)

    wishlisted_by = db.relationship("Wishlist", back_populates="product", cascade="all, delete-orphan", lazy="dynamic")
    specs = db.relationship("ProductSpec", back_populates="product", cascade="all, delete-orphan", lazy="dynamic")
    carted_by = db.relationship("Cart", back_populates="product", cascade="all, delete-orphan", lazy="dynamic")

    def __repr__(self):
        return f"<Product {self.name}>"


class ProductSpec(db.Model):
    """Модель спецификации товара"""
    __tablename__ = "product_specs"

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)

    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(255), nullable=False)

    product = db.relationship("Product", back_populates="specs")

    def __repr__(self):
        return f"<Spec {self.name}: {self.value}>"


class Wishlist(db.Model):
    """Модель списка желаний пользователя"""
    __tablename__ = "wishlists"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)

    date_added = db.Column(db.DateTime, default=datetime.now, nullable=False)

    user = db.relationship("User", back_populates="wishlists")
    product = db.relationship("Product", back_populates="wishlisted_by")

    __table_args__ = (db.UniqueConstraint('user_id', 'product_id', name='uq_user_product'),)

    def __repr__(self):
        return f"<Wishlist User: {self.user_id}, Product: {self.product_id}>"


class Cart(db.Model):
    """Модель корзины пользователя"""
    __tablename__ = "carts"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)

    quantity = db.Column(db.Integer, nullable=False, default=1)
    date_added = db.Column(db.DateTime, default=datetime.now, nullable=False)

    user = db.relationship("User", back_populates="carts")
    product = db.relationship("Product", back_populates="carted_by")

    __table_args__ = (db.UniqueConstraint('user_id', 'product_id', name='uq_user_product'),)

    def __repr__(self):
        return f"<Cart User: {self.user_id}, Product: {self.product_id}>"
