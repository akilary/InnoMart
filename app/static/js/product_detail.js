document.addEventListener("DOMContentLoaded", () => {
    initQuantityControl();
    initProductTabs();
});

/**
 * Инициализирует управление количеством товара
 */
function initQuantityControl() {
    const inputQuantity = document.getElementById("quantity");
    const btnDecrease = document.getElementById("decrease-quantity");
    const btnIncrease = document.getElementById("increase-quantity");

    if (!inputQuantity || !btnDecrease || !btnIncrease) return;

    const min = parseInt(inputQuantity.min, 10) || 1;
    const max = parseInt(inputQuantity.max, 10) || Infinity;

    btnDecrease.addEventListener("click", () => {
        let value = parseInt(inputQuantity.value, 10) || min;
        value = Math.max(min, value - 1);
        inputQuantity.value = value;
    });

    btnIncrease.addEventListener("click", () => {
        let value = parseInt(inputQuantity.value, 10) || min;
        value = Math.min(max, value + 1);
        inputQuantity.value = value;
    });
}

/**
 * Инициализирует вкладки товара, добавляя обработчики событий к кнопкам и управляя состоянием панелей
 */
function initProductTabs() {
    const tabButtons = document.querySelectorAll(".product__tabs-button");
    const tabPanels = document.querySelectorAll(".product__tabs-panel");

    tabButtons.forEach(button => {
        button.addEventListener("click", () => {
            const target = button.dataset.tab;

            tabButtons.forEach(btn => btn.classList.remove("product__tabs-button--active"));
            button.classList.add("product__tabs-button--active");

            tabPanels.forEach(panel => {
                panel.classList.toggle("product__tabs-panel--active", panel.id === target);
            });
        });
    });
}
