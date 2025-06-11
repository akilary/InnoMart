from .shared import get_user_by_id
from ..models import Product, ProductCategory, Wishlist, Cart


def get_filtered_paginated_products(
        user_id: int,
        page: int,
        per_page: int,
        categories: list[str] | None = None,
        price_min: float | None = None,
        price_max: float | None = None,
        sort_by: str | None = None
) -> dict[str, any]:
    """Возвращает товары с пагинацией и фильтрацией"""
    try:
        user = get_user_by_id(user_id) if user_id >= 0 else None

        query = Product.query
        query = _filter_products(query, price_min, price_max, categories)
        query = _sort_products(query, sort_by)

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        products = [{
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category": product.category.name,
            "image_url": product.image_url
        } for product in pagination.items]

        if user is not None:
            products = _enrich_products_with_user_data(products, user.id)

        return {
            "data": products,
            "page": page,
            "per_page": per_page,
            "total_pages": pagination.pages,
            "total_items": pagination.total,
        }
    except ValueError as e:
        raise ValueError(f"Ошибка валидации: {str(e)}")
    except Exception as e:
        raise RuntimeError("Ошибка при получении товаров") from e


def _filter_products(
        query,
        price_min: float | None = None,
        price_max: float | None = None,
        categories: list[str] | None = None
):
    """Применяет фильтры к запросу товаров"""
    try:
        if price_min is not None:
            query = query.filter(Product.price >= price_min)
        if price_max is not None:
            query = query.filter(Product.price <= price_max)
        if categories:
            matched_categories = ProductCategory.query.filter(ProductCategory.name.in_(categories)).all()
            matched_ids = [c.id for c in matched_categories]
            query = query.filter(Product.category_id.in_(matched_ids))
        return query
    except Exception as e:
        raise RuntimeError("Ошибка при фильтрации товаров") from e


def _sort_products(query, sort_by: str | None = None):
    """Сортирует товары по указанному критерию"""
    try:
        sort_mapping = {
            "price_asc": Product.price.asc(),
            "price_desc": Product.price.desc(),
            "new": Product.query.all(),
            "discount": Product.query.all(),
        }

        if sort_by in sort_mapping:
            query = query.order_by(sort_mapping[sort_by])
        return query
    except Exception as e:
        raise RuntimeError("Ошибка при сортировке товаров") from e


def _enrich_products_with_user_data(products: list[dict], user_id: int) -> list[dict]:
    """Добавляет информацию о наличии товаров в корзине и списке желаний"""
    try:
        wishlist_ids = {
            w.product_id for w in Wishlist.query.filter_by(user_id=user_id).with_entities(Wishlist.product_id).all()
        }
        cart_ids = {
            c.product_id for c in Cart.query.filter_by(user_id=user_id).with_entities(Cart.product_id).all()
        }

        for product in products:
            product["in_wishlist"] = product["id"] in wishlist_ids
            product["in_cart"] = product["id"] in cart_ids

        return products
    except Exception as e:
        raise RuntimeError("Ошибка при обогащении данных о товарах") from e


def get_all_categories() -> list[ProductCategory]:
    """Возвращает все категории товаров"""
    return [c for c in ProductCategory.query.all()]
