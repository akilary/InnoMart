import json

from werkzeug.security import generate_password_hash

from app import create_app
from app.extensions import db
from app.models import Product, ProductCategory, ProductGallery, ProductSpec, User


def _create_admin() -> None:
    """Создание администратора"""
    if not User.query.filter_by(email="admin@example.com").first():
        admin = User(
            username="admin",
            email="admin@example.com",
            password=generate_password_hash("admin123"),
            role="admin"
        )
        db.session.add(admin)
        print("Администратор добавлен")
    else:
        print("Администратор уже существует")


def _load_products(filename: str) -> dict:
    """Загрузка данных о товарах из JSON-файла"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Ошибка: Файл {filename} не найден")
        return {}
    except json.JSONDecodeError as e:
        print(f"Ошибка при чтении JSON: {e}")
        return {}


def main() -> None:
    app = create_app()

    with app.app_context():
        db.create_all()

        _create_admin()

        data = _load_products("data/products.json")
        if not data:
            print("Не удалось загрузить данные о товарах")
            return

        added_products = 0
        for category_name, category_data in data.items():
            if not isinstance(category_data, dict) or "items" not in category_data:
                print(f"Предупреждение: Категория '{category_name}' имеет неверный формат")
                continue

            category_obj = ProductCategory.query.filter_by(name=category_name).first()
            if not category_obj:
                category_obj = ProductCategory(
                    name=category_name,
                    slug=category_data.get("slug", category_name.lower().replace(" ", "-")),
                    icon=category_data.get("icon", "category")
                )
                db.session.add(category_obj)
                db.session.flush()

            products = category_data.get("items", [])
            if not isinstance(products, list):
                print(f"Предупреждение: В категории '{category_name}' товары должны быть списком")
                continue

            for product_data in products:
                try:
                    product = Product(
                        name=product_data.get("name", "Без названия"),
                        description=product_data.get("description", ""),
                        category=category_obj,
                        price=product_data.get("price", 0.0),
                        stock=product_data.get("stock", 10),
                        is_new=product_data.get("is_new", False),
                        is_promotion=product_data.get("is_promotion", False),
                        image_url=product_data.get("image_url") or Product.image_url.default.arg,
                        ozon_product_id=product_data.get("ozon_product_id", "-1"),
                    )

                    db.session.add(product)
                    db.session.flush()

                    gallery = product_data.get("gallery", [])
                    if gallery and isinstance(gallery, list):
                        for img_url in gallery:
                            if img_url and isinstance(img_url, str):
                                gallery_item = ProductGallery(
                                    image_url=img_url,
                                    product_id=product.id
                                )
                                db.session.add(gallery_item)

                    specs = product_data.get("specs", {})
                    if isinstance(specs, dict):
                        for spec_name, spec_value in specs.items():
                            if spec_name and spec_value is not None:
                                spec = ProductSpec(
                                    name=str(spec_name)[:100],
                                    value=str(spec_value)[:255],
                                    product_id=product.id
                                )
                                db.session.add(spec)

                    added_products += 1

                except Exception as e:
                    db.session.rollback()
                    print(f"Ошибка при добавлении товара {product_data.get('name')}: {e}")

        try:
            db.session.commit()
            print(f"Успешно добавлено {added_products} товаров")
        except Exception as e:
            db.session.rollback()
            print(f"Ошибка при сохранении в базу данных: {e}")


if __name__ == "__main__":
    main()
