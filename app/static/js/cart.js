import {fetchApi} from "./utils/api.js";


document.addEventListener("DOMContentLoaded", () => {
    initCartFunctionality();
});

/** Инициализирует функциональность корзины для добавления и удаления продуктов */
function initCartFunctionality() {
    document.body.addEventListener("click", async (e) => {
        const cartButton = e.target.closest(".product-card__action-button--cart, .product-card__action-button--in-cart");

        if (cartButton && !cartButton.disabled) {
            cartButton.disabled = true;

            const productId = cartButton.dataset.productId;
            const icon = cartButton.querySelector(".product-card__action-button-icon");
            const isInCart = cartButton.classList.contains("product-card__action-button--in-cart");

            try {
                const method = isInCart ? "DELETE" : "PUT";
                const res = await fetchApi(`/api/cart/${productId}`, {method});

                if (!res) return;

                if (isInCart) {
                    cartButton.classList.remove("product-card__action-button--in-cart");
                    cartButton.classList.add("product-card__action-button--cart");
                    if (icon && icon.textContent.trim() === "add_shopping_cart") {
                        icon.textContent = "remove_shopping_cart";
                    }
                } else {
                    cartButton.classList.remove("product-card__action-button--cart");
                    cartButton.classList.add("product-card__action-button--in-cart");
                    if (icon && icon.textContent.trim() === "remove_shopping_cart") {
                        icon.textContent = "add_shopping_cart";
                    }
                }

                await updateCartCounter();
            } catch (err) {
                const action = isInCart ? "удалении из" : "добавлении в";
                console.error(`%c[Cart] Ошибка при ${action} корзину:`, "color: red; font-weight: bold;", err);
            } finally {
                cartButton.disabled = false;
            }
        }
    });
}

/** Обновляет счетчик товаров в шапке */
async function updateCartCounter() {
    const cartCounter = document.getElementById("cart-quantity");
    if (cartCounter) {
        try {
            const data = await fetchApi("/api/cart/quantity", {method: "GET"});
            cartCounter.textContent = data["quantity"];
        } catch (err) {
            console.error("%c[Cart] Ошибка при обновлении счетчика:", "color: red; font-weight: bold;", err);
        }
    }
}
