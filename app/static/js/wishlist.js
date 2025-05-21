import {fetchApi} from "./utils/api.js";


document.addEventListener("DOMContentLoaded", () => {
    initWishlistFunctionality();
});

/** Инициализирует функциональность списка желаний для добавления и удаления продуктов */
function initWishlistFunctionality() {
    document.body.addEventListener("click", async (e) => {
        const wishlistButton = e.target.closest(".product-card__action-button--wishlist, .product-card__action-button--in-wishlist");

        if (wishlistButton && !wishlistButton.disabled) {
            wishlistButton.disabled = true;

            const productId = wishlistButton.dataset.productId;
            const icon = wishlistButton.querySelector(".product-card__action-button-icon");
            const isInWishlist = wishlistButton.classList.contains("product-card__action-button--in-wishlist");

            try {
                const method = isInWishlist ? "DELETE" : "PUT";
                const res = await fetchApi(`/api/wishlist/${productId}`, {method});

                if (!res) return;

                if (isInWishlist) {
                    wishlistButton.classList.remove("product-card__action-button--in-wishlist");
                    wishlistButton.classList.add("product-card__action-button--wishlist");
                    if (icon && icon.textContent.trim() === "bookmark_add") {
                        icon.textContent = "bookmark";
                    }
                } else {
                    wishlistButton.classList.remove("product-card__action-button--wishlist");
                    wishlistButton.classList.add("product-card__action-button--in-wishlist");
                    if (icon && icon.textContent.trim() === "bookmark") {
                        icon.textContent = "bookmark_add";
                    }
                }
            } catch (err) {
                const action = isInWishlist ? "удалении из" : "добавлении в";
                console.error(`%c[Wishlist] Ошибка при ${action} избранное:`, "color: red; font-weight: bold;", err);
            } finally {
                wishlistButton.disabled = false;
            }
        }
    });
}
