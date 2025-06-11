import {fetchApi, showNotification, updateCartCounter} from "../utils/utils.js";


document.addEventListener("DOMContentLoaded", () => {
    setupNavBtns();
    setupProfileModals();
    setupViewAllButtons();
    setupWishlistButtons();
    setupModals();
    setupPhoneInput();
    initOrderToggle();
});

/** Инициализация навигационных кнопок */
function setupNavBtns() {
    const buttons = document.querySelectorAll(".profile__nav-item");
    const sections = document.querySelectorAll(".profile__section");

    buttons.forEach(btn => {
        btn.addEventListener("click", () => {
            const target = btn.dataset.section;

            buttons.forEach(b => b.classList.remove("profile__nav-item--active"));
            btn.classList.add("profile__nav-item--active");

            sections.forEach(section => {
                section.classList.toggle("profile__section--active", section.id === target);
            });
        });
    });
}

/** Инициализация кнопок действий для модальных окон */
function setupProfileModals() {
    const buttons = document.querySelectorAll(
        ".profile__action-card[data-modal-target], .profile__settings-edit[data-modal-target]"
    );

    buttons.forEach(button => {
        button.addEventListener("click", () => {
            const modalId = button.dataset.modalTarget;
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.add("modal--active");
            }
        });
    });
}

/** Переключает на раздел профиля по кнопке "Все заказы" */
function setupViewAllButtons() {
    const viewAllButtons = document.querySelectorAll(".profile__view-all");
    const navButtons = document.querySelectorAll(".profile__nav-item");
    const sections = document.querySelectorAll(".profile__section");

    viewAllButtons.forEach(button => {
        button.addEventListener("click", () => {
            const target = button.dataset.section;

            navButtons.forEach(btn =>
                btn.classList.toggle("profile__nav-item--active", btn.dataset.section === target)
            );

            sections.forEach(section =>
                section.classList.toggle("profile__section--active", section.id === target)
            );
        });
    });
}

/** Инициализирует удаление и добавление в корзину в избранным */
function setupWishlistButtons() {
    document.body.addEventListener("click", async (e) => {
        const removeButton = e.target.closest(".product-card__action-button--remove");
        const cartButton = e.target.closest(".product-card__action-button--cart");

        if (removeButton && !removeButton.disabled) {
            removeButton.disabled = true;
            const productId = removeButton.dataset.productId;
            const productCard = removeButton.closest(".product-card");

            try {
                const res = await fetchApi(`/api/wishlist/${productId}`, {method: "DELETE"});
                if (!res) return;

                productCard?.remove();
                updateWishlistBadges();
                showNotification("Товар удален из избранного", "success");
            } catch (err) {
                console.error("[Wishlist] Ошибка при удалении:", err);
                showNotification("Ошибка при удалении из избранного", "error");
            } finally {
                removeButton.disabled = false;
            }
        }

        if (cartButton && !cartButton.disabled) {
            cartButton.disabled = true;
            const productId = cartButton.dataset.productId;

            try {
                const res = await fetchApi(`/api/cart/${productId}`, {method: "PUT"});
                if (!res) return;

                cartButton.classList.add("product-card__action-button--success");
                setTimeout(() => cartButton.classList.remove("product-card__action-button--success"), 1000);

                await updateCartCounter();
                showNotification("Товар добавлен в корзину", "success");
            } catch (err) {
                console.error("[Cart] Ошибка при добавлении:", err);
                showNotification("Ошибка при добавлении в корзину", "error");
            } finally {
                cartButton.disabled = false;
            }
        }
    });

    function updateWishlistBadges() {
        const badge = document.querySelector(".profile__nav-item[data-section='favorites'] .profile__nav-badge");
        const wishlistGrid = document.querySelector(".profile__wishlist-grid");
        const overviewCount = document.querySelector(".profile__stat-card:nth-child(2) .profile__stat-value");

        if (badge) {
            const count = parseInt(badge.textContent);
            if (count > 1) {
                badge.textContent = String(count - 1);
            } else {
                badge.remove();

                if (wishlistGrid && wishlistGrid.children.length === 0) {
                    wishlistGrid.remove();
                    const emptyState = `
                        <div class="profile__empty-state">
                            <span class="material-icons profile__empty-state-icon">favorite</span>
                            <p class="profile__empty-state-text">В избранном пока пусто</p>
                            <a href="/catalog" class="profile__empty-action">Перейти в каталог</a>
                        </div>
                    `;
                    document.getElementById("favorites")?.insertAdjacentHTML("beforeend", emptyState);
                }
            }
        }

        if (overviewCount) {
            const count = parseInt(overviewCount.textContent);
            overviewCount.textContent = String(Math.max(0, count - 1));
        }
    }
}

/** Инициализация модальных окон */
function setupModals() {
    document.body.addEventListener("click", (e) => {
        const closeBtn = e.target.closest(".modal__close, .modal__button[data-action='close']");
        const activeModal = e.target.closest(".modal");

        if (closeBtn && activeModal) {
            activeModal.classList.remove("modal--active");
            return;
        }

        if (e.target.classList.contains("modal") && e.target.classList.contains("modal--active")) {
            e.target.classList.remove("modal--active");
        }
    });
}


/** Инициализация обработки ввода телефона */
function setupPhoneInput() {
    const phoneInput = document.getElementById("personal-phone");
    if (phoneInput) {
        phoneInput.addEventListener("input", () => {
            const raw = phoneInput.value.replace(/\D/g, "");
            const core = raw.replace(/^7|8/, "");
            const digits = core.slice(0, 10);
            phoneInput.value = formatPhoneNum(digits);
        });
    }
}

/** Форматирование введенного номера телефона */
function formatPhoneNum(digits) {
    const parts = [digits.slice(0, 3), digits.slice(3, 6), digits.slice(6, 8), digits.slice(8, 10)];

    let result = "+7";

    if (parts[0]) result += ` (${parts[0]}`;
    if (parts[0]?.length === 3) result += `)`;
    if (parts[1]) result += ` ${parts[1]}`;
    if (parts[2]) result += `-${parts[2]}`;
    if (parts[3]) result += `-${parts[3]}`;

    return result;
}

function initOrderToggle() {
    document.body.addEventListener("click", async (e) => {
        const toggleBtn = e.target.closest(".profile__order-toggle");
        if (!toggleBtn) return;

        const orderItem = toggleBtn.closest(".profile__order-item");
        const detailsContainerId = toggleBtn.getAttribute("aria-controls");
        const detailsContainer = document.getElementById(detailsContainerId);
        if (!detailsContainer || !orderItem) return;

        const isExpanded = toggleBtn.getAttribute("aria-expanded") === "true";
        if (isExpanded) {
            toggleBtn.setAttribute("aria-expanded", "false");
            detailsContainer.hidden = true;
            return;
        }

        if (!detailsContainer.dataset.loaded) {
            try {
                const orderId = orderItem.dataset.orderId;
                const data = await fetchApi(`/api/orders/${orderId}`, {method: "GET"});

                renderOrderDetails(detailsContainer, data);
                detailsContainer.dataset.loaded = "true";
            } catch (err) {
                console.error("[Order] Failed to fetch order details", err);
                showNotification("Ошибка при получении деталей заказа", "error");
                return;
            }
        }

        toggleBtn.setAttribute("aria-expanded", "true");
        detailsContainer.hidden = false;
    });
}

function renderOrderDetails(container, order) {
    const itemsHtml = order.items.map(item => `
        <li class="order-details__item">
            <img src="${item.image_url}" alt="${item.name}" class="order-details__img">
            <div class="order-details__info">
                <a href="/product/${item.id}" class="order-details__name">${item.name}</a>
                <p class="order-details__qty">${item.quantity} × ${item.price} ₸</p>
            </div>
            <div class="order-details__total">${item.total_price} ₸</div>
        </li>
    `).join("");

    container.innerHTML = `
        <ul class="order-details__list">
            ${itemsHtml}
        </ul>
        <div class="order-details__summary">
            <span>Итого:</span>
            <span>${order.total_price} ₸</span>
        </div>
    `;
}
