import {fetchApi, showNotification, updateBadge, updateCartCounter} from "../utils/utils.js";


document.addEventListener("DOMContentLoaded", () => {
    initQuantityControl();
    initProductTabSwitching();
    initWishlistAndCartButtons();
    initGalleryImageSwitching();
});

/** Управляет кнопками изменения количества товара */
function initQuantityControl() {
    const input = document.getElementById("quantity");
    const dec = document.getElementById("decrease-quantity");
    const inc = document.getElementById("increase-quantity");

    if (!input || !dec || !inc) return;

    const min = parseInt(input.min, 10) || 1;
    const max = parseInt(input.max, 10) || Infinity;

    dec.addEventListener("click", () => {
        input.value = Math.max(min, (parseInt(input.value, 10) || min) - 1);
    });

    inc.addEventListener("click", () => {
        input.value = Math.min(max, (parseInt(input.value, 10) || min) + 1);
    });
}

/** Переключает вкладки на странице товара */
function initProductTabSwitching() {
    const buttons = document.querySelectorAll(".product__tabs-button");
    const panels = document.querySelectorAll(".product__tabs-panel");

    buttons.forEach(btn => {
        btn.addEventListener("click", () => {
            const target = btn.dataset.tab;

            buttons.forEach(b => b.classList.remove("product__tabs-button--active"));
            btn.classList.add("product__tabs-button--active");

            panels.forEach(panel => {
                panel.classList.toggle("product__tabs-panel--active", panel.id === target);
            });
        });
    });
}

/** Обрабатывает клики по кнопкам "В избранное" и "В корзину"*/
function initWishlistAndCartButtons() {
    document.body.addEventListener("click", async (e) => {
        const wishlistButton = e.target.closest(".product__button--wishlist");
        const cartButton = e.target.closest(".product__button--cart");

        if (wishlistButton && !wishlistButton.disabled) {
            await handleWishlistAction(wishlistButton);
        }

        if (cartButton && !cartButton.disabled) {
            await handleCartAction(cartButton);
            await updateCartCounter();
        }
    });
}

async function handleWishlistAction(button) {
    button.disabled = true;
    const productId = button.dataset.productId;
    const isInWishlist = button.classList.contains("product__button--in-wishlist");

    try {
        const method = isInWishlist ? "DELETE" : "PUT";
        const res = await fetchApi(`/api/wishlist/${productId}`, {method});
        if (!res) return;

        button.classList.toggle("product__button--in-wishlist", !isInWishlist);
        showNotification(isInWishlist ? "Товар удален из избранного" : "Товар добавлен в избранное", "success");
    } catch (err) {
        console.error("[Wishlist] Ошибка:", err);
        showNotification("Ошибка при обновлении избранного", "error");
    } finally {
        button.disabled = false;
    }
}

async function handleCartAction(button) {
    button.disabled = true;
    const productId = button.dataset.productId;
    const quantityInput = document.getElementById("quantity");
    const quantity = quantityInput ? parseInt(quantityInput.value, 10) : 1;

    try {
        const res = await fetchApi(`/api/cart/${productId}`, {
            method: "PUT",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({quantity})
        });
        if (!res) return;

        button.classList.add("product__button--success");
        setTimeout(() => button.classList.remove("product__button--success"), 1000);

        await updateBadge(productId, false, true);
        showNotification("Товар добавлен в корзину", "success");
    } catch (err) {
        console.error("[Cart] Ошибка:", err);
        showNotification("Ошибка при добавлении в корзину", "error");
    } finally {
        button.disabled = false;
    }
}

/** Переключает изображения в галерее */
function initGalleryImageSwitching() {
    const mainImage = document.querySelector(".product__main-image img");
    const thumbnails = document.querySelectorAll(".product__thumbnail");

    thumbnails.forEach(thumbnail => {
        thumbnail.addEventListener("click", () => {
            mainImage.src = thumbnail.querySelector("img").src;

            thumbnails.forEach(t => t.classList.remove("product__thumbnail--active"));
            thumbnail.classList.add("product__thumbnail--active");
        });
    });
}
