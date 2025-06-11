import {fetchApi, updateCartCounter, showNotification} from "../utils/utils.js";


document.addEventListener("DOMContentLoaded", () => {
    setupCartQuantity();
    attachCartActions();
    handleCartClear();
    setupCheckout();
});

/** Обработка изменения количества товаров в корзине */
function setupCartQuantity() {
    document.querySelectorAll(".cart__item").forEach(item => {
        const productId = item.dataset.productId;
        const decreaseBtn = item.querySelector(".cart__quantity-decrease");
        const increaseBtn = item.querySelector(".cart__quantity-increase");
        const quantityInput = item.querySelector(".cart__quantity-input");

        if (!decreaseBtn || !increaseBtn || !quantityInput) return;

        const updateQuantity = async (newValue) => {
            quantityInput.value = newValue;
            await patchCartQuantity(productId, newValue);
            updateItemTotal(item, newValue);
            updateSummary();
        };

        decreaseBtn.addEventListener("click", async () => {
            const value = parseInt(quantityInput.value);
            if (value > 1) {
                await updateQuantity(value - 1);
            } else if (confirm("Удалить товар из корзины?")) {
                await removeItem(productId);
            }
        });

        increaseBtn.addEventListener("click", async () => {
            const value = parseInt(quantityInput.value);
            await updateQuantity(value + 1);
        });

        quantityInput.addEventListener("change", async () => {
            let value = parseInt(quantityInput.value);
            if (isNaN(value) || value < 1) value = 1;
            await updateQuantity(value);
        });
    });
}

/** Обработчики "удалить" и "в избранное" */
function attachCartActions() {
    document.querySelectorAll(".cart__item").forEach(item => {
        const productId = item.dataset.productId;

        item.querySelector(".cart__item-action--remove")?.addEventListener("click", async () => {
            if (confirm("Удалить товар из корзины?")) {
                await removeItem(productId);
            }
        });

        item.querySelector(".cart__item-action--wishlist")?.addEventListener("click", async () => {
            try {
                await fetchApi(`/api/wishlist/${productId}`, {method: "PUT"});
                showNotification("Товар добавлен в избранное", "success");
            } catch (error) {
                if (error.message.includes("уже добавлен")) {
                    showNotification("Товар уже в избранном", "info");
                } else {
                    showNotification("Ошибка при добавлении в избранное", "error");
                    console.error("Ошибка при добавлении в избранное:", error);
                }
            }
        });
    });
}

/** Очистка корзины */
function handleCartClear() {
    document.getElementById("clear-cart")?.addEventListener("click", async () => {
        if (!confirm("Вы уверены, что хотите очистить корзину?")) return;

        try {
            await fetchApi("/api/cart", {method: "DELETE"});
            showNotification("Корзина очищена", "success");
            window.location.reload();
        } catch (error) {
            showNotification("Ошибка при очистке корзины", "error");
            console.error("Ошибка при очистке корзины:", error);
        }
    });
}

/** Оформление заказа */
function setupCheckout() {
    document.getElementById("checkout-button")?.addEventListener("click", async () => {
        try {
            await fetchApi("/api/orders", {method: "POST"});
            showNotification("Заказ успешно оформлен!", "success");
            window.location.href = "/profile";
        } catch (error) {
            showNotification(error.message, "warning");
        }
    });
}

/** Обновляет количество товара в корзине */
async function patchCartQuantity(productId, quantity) {
    try {
        await fetchApi(`/api/cart/${productId}`, {
            method: "PATCH",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({quantity})
        });

        await updateCartCounter();
    } catch (error) {
        showNotification("Ошибка при обновлении количества", "error");
        console.error("Ошибка при обновлении количества:", error);
    }
}

/** Удаление товара из корзины */
async function removeItem(productId) {
    try {
        await fetchApi(`/api/cart/${productId}`, {method: "DELETE"});

        document.querySelector(`.cart__item[data-product-id="${productId}"]`)?.remove();

        await updateCartCounter();
        updateSummary();

        if (!document.querySelector(".cart__item")) {
            window.location.reload();
        }

        showNotification("Товар удален из корзины", "success");
    } catch (error) {
        showNotification("Ошибка при удалении товара", "error");
        console.error("Ошибка при удалении товара:", error);
    }
}

/** Обновление суммы за товар */
function updateItemTotal(cartItem, quantity) {
    const priceText = cartItem.querySelector(".cart__item-price")?.textContent;
    const price = parseFloat(priceText);

    if (!isNaN(price)) {
        cartItem.setAttribute("data-total-price", price * quantity);
    }
}

/** Пересчёт суммы корзины */
function updateSummary() {
    let subtotal = 0;

    document.querySelectorAll(".cart__item").forEach(item => {
        const quantity = parseInt(item.querySelector(".cart__quantity-input")?.value || 0);
        const price = parseFloat(item.querySelector(".cart__item-price")?.textContent || 0);
        subtotal += price * quantity;
    });

    const shipping = subtotal >= 20000 ? 0 : 1500;
    const total = subtotal + shipping;

    const setText = (id, value) => {
        const el = document.getElementById(id);
        if (el) el.textContent = `${value} ₸`;
    };

    setText("cart-subtotal", subtotal.toFixed(2));
    setText("cart-shipping", shipping);
    setText("cart-total", total.toFixed(2));
}

