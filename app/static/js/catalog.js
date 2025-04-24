import {fetchApi} from "./utils/api.js";

let currentPage = 1;
const perPage = 20;

document.addEventListener("DOMContentLoaded", async () => {
    initProductLoading(document.getElementById("load-more"));
    initFilters(document.getElementById("filter-form"));
    try {
        await loadProducts();
    } catch (err) {
        console.error("%c[Init] Не удалось загрузить товары:", "color: red; font-weight: bold;", err);
    }

    initSearch();
    initToggleFilters();

    new Choices(document.getElementById("filter-select"), {
        searchEnabled: false,
        itemSelectText: "",
        shouldSort: false,
    });
});

/**
 * Добавляет слушатель событий, чтобы загрузить больше продуктов при нажатии
 */
function initProductLoading(loadMoreButton) {
    if (loadMoreButton) {
        loadMoreButton.addEventListener("click", () => loadProducts());
    }
}

/**
 * Инициализирует кнопки "Применить фильтры" и "Сбросить фильтры"
 */
function initFilters(filterForm) {
    if (!filterForm) return;

    const applyButton = document.getElementById("apply-filters");
    if (applyButton) {
        applyButton.addEventListener("click", async (e) => {
            e.preventDefault();
            currentPage = 1;
            try {
                await loadProducts(true);
            } catch (err) {
                console.error("%c[Filters] Ошибка при применении фильтров:", "color: orange; font-weight: bold;", err);
            }
        });
    }

    const resetButton = document.getElementById("reset-filters");
    if (resetButton) {
        resetButton.addEventListener("click", async () => {
            filterForm.reset();
            currentPage = 1;
            try {
                await loadProducts(true);
            } catch (err) {
                console.error("%c[Filters] Ошибка при сбросе фильтров:", "color: orange; font-weight: bold;", err);
            }
        });
    }
}

/**
 * Загружает продукты с сервера и добавляет их в контейнер продукта
 */
async function loadProducts(reset = false) {
    const container = document.getElementById("products-container");
    const productsCount = document.getElementById("products-count");
    const loadingIndicator = document.getElementById("loading-indicator");
    if (!container) return;

    if (loadingIndicator) loadingIndicator.style.display = "flex";

    let url = `/api/products?page=${currentPage}&per_page=${perPage}`;
    const filterForm = document.getElementById("filter-form");
    if (filterForm) {
        const formData = new FormData(filterForm);
        const params = new URLSearchParams();

        for (const [key, value] of formData.entries()) {
            if (value instanceof File) continue;
            params.append(key, value);
        }
        url += `&${params.toString()}`;
    }

    try {
        const result = await fetchApi(url, {method: "GET"});
        if (result.html) {
            if (reset) container.innerHTML = "";
            container.insertAdjacentHTML("beforeend", result.html);
        }

        if (productsCount && result["total_items"] !== undefined) {
            productsCount.textContent = `Найдено товаров: ${result["total_items"]}`;
        }

        currentPage++;

        const loadMoreButton = document.getElementById("load-more");
        if (loadMoreButton) {
            loadMoreButton.style.display =
                result.page >= result["total_pages"] ? "none" : "inline-flex";
        }
    } catch (err) {
        console.error("Ошибка при загрузке товаров", err);
    } finally {
        if (loadingIndicator) loadingIndicator.style.display = "none";
    }
}

/**
 * Реализует клиентский поиск по заголовкам карточек товаров
 */
function initSearch() {
    const searchInput = document.getElementById("catalog-search");
    const productsContainer = document.getElementById("products-container");
    if (!searchInput || !productsContainer) return;

    searchInput.addEventListener("input", function () {
        const query = this.value.trim().toLowerCase();
        const cards = productsContainer.querySelectorAll(".product-card");
        let visibleCount = 0;

        cards.forEach((card) => {
            const titleEl = card.querySelector(".product-card__title");
            if (!titleEl) return;
            const text = titleEl.textContent.trim().toLowerCase();
            if (text.includes(query)) {
                card.style.display = "";
                visibleCount++;
            } else {
                card.style.display = "none";
            }
        });

        const productsCount = document.getElementById("products-count");
        if (productsCount) {
            productsCount.textContent = `Найдено товаров: ${visibleCount}`;
        }
    });
}

/**
 * Инициализирует переключение отображения блока фильтров
 */
function initToggleFilters() {
    const toggleButton = document.getElementById("catalog-toggle-filters");
    const catalogFilters = document.getElementById("catalog-filters");
    const toggleIcon = toggleButton?.querySelector(".material-icons");
    const toggleText = document.getElementById("toggle-text");
    if (!toggleButton || !catalogFilters || !toggleText) return;

    let isFiltersOpen = true;
    toggleButton.addEventListener("click", () => {
        isFiltersOpen = !isFiltersOpen;
        updateFiltersUI();
    });

    function updateFiltersUI() {
        catalogFilters.hidden = !isFiltersOpen;
        toggleText.textContent = isFiltersOpen
            ? "Скрыть фильтры"
            : "Показать фильтры";
        toggleButton.setAttribute("aria-expanded", isFiltersOpen);
        if (toggleIcon) {
            toggleIcon.textContent = isFiltersOpen ? "close" : "tune";
        }
    }

    updateFiltersUI();
}
