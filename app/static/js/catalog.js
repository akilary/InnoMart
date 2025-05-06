import {fetchApi} from "./utils/api.js";

/** Инициализирует загрузку продуктов с сервера */
const initProductLoader = () => {
    let currentPage = 1;
    const perPage = 20;

    /** Загружает продукты с сервера и добавляет их в контейнер продукта */
    const loadProducts = async (reset = false) => {
        if (reset) currentPage = 1;
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
    };

    /** Инициализирует кнопку "Загрузить еще" */
    const initLoadMoreButton = () => {
        const loadMoreButton = document.getElementById("load-more");
        if (loadMoreButton) {
            loadMoreButton.addEventListener("click", () => loadProducts());
        }
    };

    initLoadMoreButton();

    return {
        loadProducts
    };
};
/** Инициализирует фильтры каталога */
const initFilters = (productLoader) => {
    const filterForm = document.getElementById("filter-form");
    if (!filterForm) return;

    /** Обработчик применения фильтров */
    const applyFilters = async (e) => {
        if (e) e.preventDefault();
        try {
            await productLoader.loadProducts(true);
        } catch (err) {
            console.error("%c[Filters] Ошибка при применении фильтров:", "color: orange; font-weight: bold;", err);
        }
    };

    /** Обработчик сброса фильтров */
    const resetFilters = async () => {
        filterForm.reset();
        initChoices(true);
        try {
            await productLoader.loadProducts(true);
        } catch (err) {
            console.error("%c[Filters] Ошибка при сбросе фильтров:", "color: orange; font-weight: bold;", err);
        }
    };

    const applyButton = document.getElementById("apply-filters");
    if (applyButton) {
        applyButton.addEventListener("click", applyFilters);
    }

    const resetButton = document.getElementById("reset-filters");
    if (resetButton) {
        resetButton.addEventListener("click", resetFilters);
    }
};

/** Инициализирует функцию поиска по каталогу */
const initSearch = () => {
    const searchInput = document.getElementById("catalog-search");
    const productsContainer = document.getElementById("products-container");
    if (!searchInput || !productsContainer) return;

    /** Выполняет поиск по заголовкам карточек товаров */
    const performSearch = (query) => {
        const cards = productsContainer.querySelectorAll(".product-card");
        let visibleCount = 0;

        cards.forEach((card) => {
            const titleEl = card.querySelector(".product-card__title");
            if (!titleEl) return;

            const text = titleEl.textContent.trim().toLowerCase();
            const isVisible = text.includes(query.toLowerCase());

            card.style.display = isVisible ? "" : "none";
            if (isVisible) visibleCount++;
        });

        const productsCount = document.getElementById("products-count");
        if (productsCount) {
            productsCount.textContent = `Найдено товаров: ${visibleCount}`;
        }
    };

    searchInput.addEventListener("input", (e) => {
        const query = e.target.value.trim();
        performSearch(query);
    });
};

/** Инициализирует переключение отображения блока фильтров */
const initToggleFilters = () => {
    const toggleButton = document.getElementById("catalog-toggle-filters");
    const catalogFilters = document.getElementById("catalog-filters");
    const toggleIcon = toggleButton?.querySelector(".material-icons");
    const toggleText = document.getElementById("toggle-text");

    if (!toggleButton || !catalogFilters || !toggleText) return;

    let isFiltersOpen = true;

    /** Обновляет UI фильтров в соответствии с текущим состоянием */
    const updateFiltersUI = () => {
        if (!isFiltersOpen) {
            catalogFilters.classList.add("catalog__filters--collapsed");
            catalogFilters.setAttribute("aria-hidden", "true");
        } else {
            catalogFilters.classList.remove("catalog__filters--collapsed");
            catalogFilters.setAttribute("aria-hidden", "false");
        }

        toggleText.textContent = isFiltersOpen
            ? "Скрыть фильтры"
            : "Показать фильтры";

        toggleButton.setAttribute("aria-expanded", isFiltersOpen);

        if (toggleIcon) {
            toggleIcon.textContent = isFiltersOpen ? "close" : "tune";
        }
    };

    /** Переключает состояние отображения фильтров */
    const toggleFilters = () => {
        isFiltersOpen = !isFiltersOpen;
        updateFiltersUI();
    };

    toggleButton.addEventListener("click", toggleFilters);

    updateFiltersUI();
};

let choicesInstance;
/** Инициализирует компоненты выбора Choices.js */
const initChoices = (reset = false) => {
    const filterSelect = document.getElementById("filter-select");

    if (filterSelect && !choicesInstance) {
        choicesInstance = new Choices(filterSelect, {
            searchEnabled: false,
            itemSelectText: "",
            shouldSort: false,
        });
    }

    if (reset && choicesInstance) choicesInstance.removeActiveItems();
};

/** Главная функция инициализации каталога */
const init = async () => {
    try {
        const productLoader = initProductLoader();

        initFilters(productLoader);

        await productLoader.loadProducts();

        initSearch();
        initToggleFilters();
        initChoices();
    } catch (err) {
        console.error("%c[Catalog] Ошибка инициализации каталога:", "color: red; font-weight: bold;", err);
    }
};


document.addEventListener("DOMContentLoaded", init);
