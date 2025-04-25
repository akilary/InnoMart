document.addEventListener("DOMContentLoaded", () => {
    initNavButtons();
    initQuickActionButtons();
    initPhoneInput();
    initPasswordToggle();
});


/**
 * Инициализация навигационных кнопок
 */
function initNavButtons() {
    const navButtons = document.querySelectorAll(".profile__nav-item");
    const sections = document.querySelectorAll(".profile__section");

    navButtons.forEach(button => {
        button.addEventListener("click", () => {
            const target = button.dataset.section;

            navButtons.forEach(btn => btn.classList.remove("profile__nav-item--active"));
            button.classList.add("profile__nav-item--active");

            sections.forEach(section => {
                section.classList.toggle("profile__section--active", section.id === target);
            });
        });
    });
}

/**
 * Инициализация кнопок действий для модальных окон
 */
function initQuickActionButtons() {
    const quickActionButtons = document.querySelectorAll(".profile__action-card");
    quickActionButtons.forEach(button => {
        button.addEventListener("click", function() {
            const action = this.dataset.modalTarget;
            switch (action) {
                case "personalModal":
                    alert("Откроется модальное окно для редактирования персональных данных.");
                    break;
                case "addressModal":
                    alert("Откроется модальное окно для редактирования адреса доставки.");
                    break;
            }
        });
    });
}

/**
 * Инициализация обработки ввода телефона
 */
function initPhoneInput() {
    const phoneInput = document.getElementById("update-phone");
    phoneInput.addEventListener("input", () => {
        const raw = phoneInput.value.replace(/\D/g, "");
        const core = raw.replace(/^7|8/, "");
        const digits = core.slice(0, 10);
        phoneInput.value = formatPhone(digits);
    });
}

/**
 * Форматирование введенного номера телефона
 */
function formatPhone(digits) {
    const parts = [
        digits.slice(0, 3),
        digits.slice(3, 6),
        digits.slice(6, 8),
        digits.slice(8, 10)
    ];

    let result = "+7";

    if (parts[0]) result += ` (${parts[0]}`;
    if (parts[0]?.length === 3) result += `)`;
    if (parts[1]) result += ` ${parts[1]}`;
    if (parts[2]) result += `-${parts[2]}`;
    if (parts[3]) result += `-${parts[3]}`;

    return result;
}

/**
 * Инициализация обработки переключателя видимости пароля
 */
function initPasswordToggle() {
    const toggleButtons = document.querySelectorAll(".auth__password-toggle");
    toggleButtons.forEach(button => {
        button.addEventListener("click", () => {
            const input = button.previousElementSibling;
            if (input.type === "password") {
                input.type = "text";
                button.querySelector("span").textContent = "visibility_off";
            } else {
                input.type = "password";
                button.querySelector("span").textContent = "visibility";
            }
        });
    });
}