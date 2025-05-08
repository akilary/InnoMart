import {fetchApi} from "./utils/api.js";

/** Инициализирует функциональность добавления товаров в корзину */
const initAddCart = () => {
    document.body.addEventListener("click", async (e) => {
        const addCartButton = e.target.closest(".product-card__action-button--cart");
        if (addCartButton && !addCartButton.disabled) {
            addCartButton.disabled = true;

            const productId = addCartButton.dataset.productId;
            const icon = addCartButton.querySelector(".product-card__action-button-icon");

            try {
                await fetchApi(`/api/cart/${productId}`, {method: "PUT"});
                addCartButton.classList.remove("product-card__action-button--cart");
                addCartButton.classList.add("product-card__action-button--in-cart");
                if (icon) {
                    icon.textContent = icon.textContent.trim() === "remove_shopping_cart"
                        ? "add_shopping_cart"
                        : "remove_shopping_cart";
                }
            } catch (err) {
                console.error("%c[Wishlist] Ошибка при добавлении в корзину:", "color: red; font-weight: bold;", err);
            } finally {
                addCartButton.disabled = false;
            }
        }
    });
}

/** Инициализирует функциональность удаления товаров из корзины */
const initRemoveCart = () => {
    document.body.addEventListener("click", async (e) => {
        const removeCartButton = e.target.closest(".product-card__action-button--in-cart");
        if (removeCartButton && !removeCartButton.disabled) {
            removeCartButton.disabled = true;

            const productId = removeCartButton.dataset.productId;
            const icon = removeCartButton.querySelector(".product-card__action-button-icon");

            try {
                await fetchApi(`/api/cart/${productId}`, {method: "DELETE"});
                removeCartButton.classList.remove("product-card__action-button--in-cart");
                removeCartButton.classList.add("product-card__action-button--cart");
                if (icon) {
                    icon.textContent = icon.textContent.trim() === "add_shopping_cart"
                        ? "remove_shopping_cart"
                        : "add_shopping_cart";
                }
            } catch (err) {
                console.error("%c[Wishlist] Ошибка при удалении из корзины:", "color: red; font-weight: bold;", err);
            } finally {
                removeCartButton.disabled = false;
            }
        }
    });
}

/** Главная функция инициализации функциональности корзины */
const init = () => {
    initAddCart()
    initRemoveCart()
}

document.addEventListener("DOMContentLoaded", init);
