from ..models import Product, Wishlist


def get_filtered_paginated_products(
        page: int,
        per_page: int,
        price_min: float | None,
        price_max: float | None,
        categories: list[str] | None,
        sort_by: str | None,
        user_id: int | None
) -> dict[str, any]:
    """Возвращает товары с пагинацией и фильтрацией"""
    query = Product.query

    if price_min is not None:
        query = query.filter(Product.price >= price_min)
    if price_max is not None:
        query = query.filter(Product.price <= price_max)
    if categories:
        query = query.filter(Product.category.in_(categories))

    sort_mapping = {
        "price_asc": Product.price.asc(),
        "price_desc": Product.price.desc(),
        "new": Product.query.all(),
        "discount": Product.query.all()
    }

    if sort_by in sort_mapping and sort_mapping[sort_by] is not None:
        query = query.order_by(sort_mapping[sort_by])

    wishlist_ids = set()
    if user_id:
        wishlist_ids = {
            w.product_id for w in Wishlist.query.filter_by(user_id=user_id).with_entities(Wishlist.product_id).all()
        }

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    products = [{
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "category": product.category,
        "image_url": product.image_url,
        "in_wishlist": product.id in wishlist_ids,
    } for product in pagination.items]

    return {
        "data": products,
        "page": page,
        "per_page": per_page,
        "total_pages": pagination.pages,
        "total_items": pagination.total,
    }


def get_product(product_id: int) -> Product:
    """Возвращает информацию о продукте"""
    product = Product.query.get(product_id)
    if not product:
        raise ValueError(f"Продукт c ID {product_id} не найден")

    return product