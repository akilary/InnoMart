import json

from werkzeug.security import generate_password_hash

from app import create_app
from app.extensions import db
from app.models import Product, ProductSpec, User

app = create_app()

with app.app_context():
    db.create_all()

    db.session.add(
        User(
            username="admin",
            email="admin@example.com",
            password=generate_password_hash("admin123"),
            role="admin"
        )
    )
    print("Администратор добавлен")

    try:
        data = json.load(open("data/products.json", "r", encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise f"Ошибка: {e}"

    for category, products in data.items():
        for product in products:
            prod = Product(
                name=product["name"],
                description=product["description"],
                category=category,
                price=product["price"],
                image_url=product["image"]
            )

            db.session.add(prod)
            db.session.flush()

            for spec_name, spec_value in product["specs"].items():
                db.session.add(
                    ProductSpec
                        (
                        name=spec_name,
                        value=spec_value,
                        product_id=prod.id
                    )
                )

    db.session.commit()
    print("База данных успешно создана!")
