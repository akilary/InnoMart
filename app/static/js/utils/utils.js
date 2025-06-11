import {updateBadge} from './badge.js';
import {showNotification} from './notifications.js';
import {fetchApi} from './api.js';


/** Обновляет счетчик товаров в шапке */
export async function updateCartCounter() {
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

export {updateBadge};
export {showNotification};
export {fetchApi};
