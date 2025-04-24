import json

from app import create_app
from app.extensions import db
from app.models import Product, ProductSpec

app = create_app()


with app.app_context():
    db.create_all()
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
                spec = ProductSpec(
                    name=spec_name,
                    value=spec_value,
                    product_id=prod.id
                )
                db.session.add(spec)

    db.session.commit()
    print("База данных успешно создана!")
