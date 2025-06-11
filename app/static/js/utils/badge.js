/** Обновляет бейдж на карточке товара по состоянию избранного и корзины */
export function updateBadge(productId, inWishlist, inCart) {
    const badgeId = `badge-${productId}`;
    const badge = document.getElementById(badgeId);

    let label = "";
    let classes = "product-card__badge";

    if (inWishlist && inCart) {
        label = "В избранном и в корзине";
        classes += " product-card__badge--in-wishlist product-card__badge--in-cart";
    } else if (inWishlist) {
        label = "В избранном";
        classes += " product-card__badge--in-wishlist";
    } else if (inCart) {
        label = "В корзине";
        classes += " product-card__badge--in-cart";
    }

    if (label) {
        if (badge) {
            badge.textContent = label;
            badge.className = classes;
        } else {
            const imgWrapper = document.querySelector(
                `[data-product-id="${productId}"]`)?.closest(".product-card__img-wrapper"
            );
            if (imgWrapper) {
                const newBadge = document.createElement("mark");
                newBadge.className = classes;
                newBadge.id = badgeId;
                newBadge.setAttribute("aria-label", label);
                newBadge.textContent = label;
                imgWrapper.prepend(newBadge);
            }
        }
    } else if (badge) {
        badge.remove();
    }
}