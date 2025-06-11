import {fetchApi, showNotification, updateBadge, updateCartCounter} from "../utils/utils.js";


document.addEventListener("DOMContentLoaded", async () => {
    await initCatalog();
    initWishlist();
    initCart();
});

let choicesInstance;

/** Главная функция инициализации каталога */
async function initCatalog() {
    try {
        const productLoader = createProductLoader();
        setupFilters(productLoader);
        await productLoader.loadProducts();
        setupSearchFilter();
        setupFilterToggle();
        initChoices();
    } catch (err) {
        console.error("%c[Catalog] Ошибка инициализации каталога:", "color: red; font-weight: bold;", err);
    }
}

/** Загрузка и отображение товаров с пагинацией */
function createProductLoader() {
    let currentPage = 1;
    const perPage = 10;

    async function loadProducts(reset = false) {
        if (reset) currentPage = 1;

        const container = document.getElementById("products-container");
        const productsCount = document.getElementById("products-count");
        const loadingIndicator = document.getElementById("loading-indicator");
        if (!container) return;

        loadingIndicator && (loadingIndicator.style.display = "flex");

        const filterForm = document.getElementById("filter-form");
        const params = new URLSearchParams();

        if (filterForm) {
            new FormData(filterForm).forEach((value, key) => {
                if (!(value instanceof File)) params.append(key, value);
            });
        }

        const url = `/api/products?page=${currentPage}&per_page=${perPage}&${params.toString()}`;

        try {
            const result = await fetchApi(url);

            if (result.html) {
                if (reset) container.innerHTML = "";
                container.insertAdjacentHTML("beforeend", result.html);
            }

            if (productsCount && typeof result["total_items"] !== "undefined") {
                productsCount.textContent = `Найдено товаров: ${result["total_items"]}`;
            }

            currentPage++;

            const loadMoreButton = document.getElementById("load-more");
            if (loadMoreButton) {
                loadMoreButton.style.display = result.page >= result["total_pages"] ? "none" : "inline-flex";
            }
        } catch (err) {
            console.error("%c[Products] Ошибка при загрузке товаров:", "color: red; font-weight: bold;", err);
        } finally {
            loadingIndicator && (loadingIndicator.style.display = "none");
        }
    }

    document.getElementById("load-more")?.addEventListener("click", () => loadProducts());

    return {loadProducts};
}

/** Настройка фильтров каталога с применением и сбросом */
function setupFilters(productLoader) {
    const filterForm = document.getElementById("filter-form");
    if (!filterForm) return;

    async function applyFilters(e) {
        e?.preventDefault();
        try {
            await productLoader.loadProducts(true);
        } catch (err) {
            console.error("[Filters] Ошибка при применении фильтров:", err);
        }
    }

    async function resetFilters() {
        filterForm.reset();
        initChoices(true);
        try {
            await productLoader.loadProducts(true);
        } catch (err) {
            console.error("[Filters] Ошибка при сбросе фильтров:", err);
        }
    }

    document.getElementById("apply-filters")?.addEventListener("click", applyFilters);
    document.getElementById("reset-filters")?.addEventListener("click", resetFilters);
}

/** Фильтрует товары каталога по поисковому запросу */
function setupSearchFilter() {
    const searchInput = document.getElementById("catalog-search");
    const productsContainer = document.getElementById("products-container");
    if (!searchInput || !productsContainer) return;

    searchInput.addEventListener("input", e => {
        const query = e.target.value.trim().toLowerCase();
        const cards = Array.from(productsContainer.querySelectorAll(".product-card"));
        let visibleCount = 0;

        const matched = [];
        const unmatched = [];

        cards.forEach(card => {
            const title = card.querySelector(".product-card__title")?.textContent.toLowerCase() || "";
            if (title.includes(query)) {
                matched.push(card);
                visibleCount++;
            } else {
                unmatched.push(card);
            }
        });

        productsContainer.innerHTML = "";
        matched.forEach(card => {
            card.style.display = "block";
            productsContainer.appendChild(card);
        });
        unmatched.forEach(card => {
            card.style.display = "none";
            productsContainer.appendChild(card);
        });

        const productsCount = document.getElementById("products-count");
        if (productsCount) {
            productsCount.textContent = `Найдено товаров: ${visibleCount}`;
        }
    });
}


/** Управляет сворачиванием и разворачиванием блока фильтров */
function setupFilterToggle() {
    const toggleBtn = document.getElementById("catalog-toggle-filters");
    const filtersBlock = document.getElementById("catalog-filters");
    const toggleIcon = toggleBtn?.querySelector(".material-icons");
    const toggleText = document.getElementById("toggle-text");

    if (!toggleBtn || !filtersBlock || !toggleText) return;

    let isOpen = true;

    function updateUI() {
        filtersBlock.classList.toggle("catalog__filters--collapsed", !isOpen);
        filtersBlock.setAttribute("aria-hidden", (!isOpen).toString());
        toggleText.textContent = isOpen ? "Скрыть фильтры" : "Показать фильтры";
        toggleBtn.setAttribute("aria-expanded", isOpen);
        if (toggleIcon) toggleIcon.textContent = isOpen ? "close" : "tune";
    }

    function toggle() {
        isOpen = !isOpen;
        updateUI();
    }

    toggleBtn.addEventListener("click", toggle);
    updateUI();
}

/** Инициализирует компоненты выбора Choices.js */
function initChoices(reset = false) {
    const filterSelect = document.getElementById("filter-select");

    if (filterSelect && !choicesInstance) {
        choicesInstance = new Choices(filterSelect, {
            searchEnabled: false,
            itemSelectText: "",
            shouldSort: false,
        });
    }

    if (reset && choicesInstance) choicesInstance.removeActiveItems();
}

/** Инициализирует обработку добавления и удаления товаров из списка желаний */
function initWishlist() {
    document.body.addEventListener("click", async (e) => {
        const btn = e.target.closest(".product-card__action-button--wishlist, .product-card__action-button--in-wishlist");
        if (!btn || btn.disabled) return;

        btn.disabled = true;
        const productId = btn.dataset.productId;
        const icon = btn.querySelector(".product-card__action-button-icon");
        const isAdded = btn.classList.contains("product-card__action-button--in-wishlist");

        try {
            const method = isAdded ? "DELETE" : "PUT";
            const res = await fetchApi(`/api/wishlist/${productId}`, {method});
            if (!res) return;

            if (icon) icon.textContent = isAdded ? "bookmark_add" : "bookmark";

            btn.classList.toggle("product-card__action-button--in-wishlist", !isAdded);
            btn.classList.toggle("product-card__action-button--wishlist", isAdded);

            showNotification(
                isAdded ? "Товар удален из избранного" : "Товар добавлен в избранное",
                "success"
            );

        } catch (err) {
            const action = isAdded ? "удалении из" : "добавлении в";
            console.error(`%c[Wishlist] Ошибка при ${action} избранное:`, "color: red; font-weight: bold;", err);
            showNotification(`Ошибка при ${action} избранное`, "error");
        } finally {
            const cardWrapper = btn.closest(".product-card__img-wrapper");
            updateBadge(
                productId,
                !!cardWrapper.querySelector(".product-card__action-button--in-wishlist"),
                !!cardWrapper.querySelector(".product-card__action-button--in-cart")
            );
            btn.disabled = false;
        }
    });
}

/** Инициализирует обработку добавления и удаления товаров из корзины */
function initCart() {
    document.body.addEventListener("click", async (e) => {
        const btn = e.target.closest(".product-card__action-button--cart, .product-card__action-button--in-cart");
        if (!btn || btn.disabled) return;

        btn.disabled = true;
        const productId = btn.dataset.productId;
        const icon = btn.querySelector(".product-card__action-button-icon");
        const isInCart = btn.classList.contains("product-card__action-button--in-cart");

        try {
            const method = isInCart ? "DELETE" : "PUT";
            const res = await fetchApi(`/api/cart/${productId}`, {method});
            if (!res) return;

            if (icon) icon.textContent = isInCart ? "add_shopping_cart" : "remove_shopping_cart";

            btn.classList.toggle("product-card__action-button--in-cart", !isInCart);
            btn.classList.toggle("product-card__action-button--cart", isInCart);

            showNotification(
                isInCart ? "Товар удален из корзины" : "Товар добавлен в корзину",
                "success"
            );

            await updateCartCounter();
        } catch (err) {
            const action = isInCart ? "удалении из" : "добавлении в";
            console.error(`%c[Cart] Ошибка при ${action} корзину:`, "color: red; font-weight: bold;", err);
            showNotification(`Ошибка при ${action} корзину`, "error");
        } finally {
            const cardWrapper = btn.closest(".product-card__img-wrapper");
            updateBadge(
                productId,
                !!cardWrapper.querySelector(".product-card__action-button--in-wishlist"),
                !!cardWrapper.querySelector(".product-card__action-button--in-cart")
            );
            btn.disabled = false;
        }
    });
}
