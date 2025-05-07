import {fetchApi} from "./utils/api.js";

/** Инициализирует функциональность добавления товаров в избранное */
const initAddWishlist = () => {
    document.body.addEventListener("click", async (e) => {
        const addWishlistButton = e.target.closest(".product-card__action-button--wishlist");
        if (addWishlistButton && !addWishlistButton.disabled) {
            addWishlistButton.disabled = true;

            const productId = addWishlistButton.dataset.productId;
            const icon = addWishlistButton.querySelector(".product-card__action-button-icon");

            try {
                await fetchApi(`/api/wishlist/${productId}`, {method: "PUT"});
                addWishlistButton.classList.remove("product-card__action-button--wishlist");
                addWishlistButton.classList.add("product-card__action-button--in-wishlist");
                if (icon) {
                    icon.textContent = icon.textContent.trim() === "bookmark"
                        ? "bookmark_add"
                        : "bookmark";
                }
            } catch (err) {
                console.error("%c[Wishlist] Ошибка при добавлении в избранное:", "color: red; font-weight: bold;", err);
            } finally {
                addWishlistButton.disabled = false;
            }
        }
    });
}

/** Инициализирует функциональность удаления товаров из избранного */
const initRemoveWishlist = () => {
    document.body.addEventListener("click", async (e) => {
        const removeWishlistButton = e.target.closest(".product-card__action-button--in-wishlist");
        if (removeWishlistButton && !removeWishlistButton.disabled) {
            removeWishlistButton.disabled = true;

            const productId = removeWishlistButton.dataset.productId;
            const icon = removeWishlistButton.querySelector(".product-card__action-button-icon");

            try {
                await fetchApi(`/api/wishlist/${productId}`, {method: "DELETE"});
                removeWishlistButton.classList.remove("product-card__action-button--in-wishlist");
                removeWishlistButton.classList.add("product-card__action-button--wishlist");
                if (icon) {
                    icon.textContent = icon.textContent.trim() === "bookmark_add"
                        ? "bookmark"
                        : "bookmark_add";
                }
            } catch (err) {
                console.error("%c[Wishlist] Ошибка при удалении из избранного:", "color: red; font-weight: bold;", err);
            } finally {
                removeWishlistButton.disabled = false;
            }
        }
    });
}

/** Главная функция инициализации функциональности избранного */
const init = () => {
    initAddWishlist()
    initRemoveWishlist()
}

document.addEventListener("DOMContentLoaded", init);
