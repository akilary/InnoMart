document.addEventListener('DOMContentLoaded', () => {
    // Открытие модалки
    document.querySelectorAll('[data-modal-target]').forEach(button => {
        button.addEventListener('click', () => {
            const modalId = button.getAttribute('data-modal-target');
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.add('active');
                modal.setAttribute('aria-hidden', 'false');
            }
        });
    });

    // Закрытие модалок
    document.querySelectorAll('.modal').forEach(modal => {
        const closeButtons = modal.querySelectorAll('[data-modal-close]');
        closeButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                modal.classList.remove('active');
                modal.setAttribute('aria-hidden', 'true');
            });
        });

        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('active');
                modal.setAttribute('aria-hidden', 'true');
            }
        });
    });

    // Форматирование номера телефона
    const phoneInput = document.getElementById("update-phone");
    phoneInput.addEventListener("input", () => {
        const raw = phoneInput.value.replace(/\D/g, "");

        const core = raw.replace(/^7|8/, "");
        const digits = core.slice(0, 10);

        phoneInput.value = formatPhone(digits);
    });

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

    // Переключение между разделами профиля
    const navItems = document.querySelectorAll('.profile__nav-item');
    const sections = document.querySelectorAll('.profile__section');

    navItems.forEach(item => {
        item.addEventListener('click', function() {
            const targetId = this.dataset.section;

            // Обновляем активный класс для навигации
            navItems.forEach(nav => nav.classList.remove('profile__nav-item--active'));
            this.classList.add('profile__nav-item--active');

            // Показываем соответствующий раздел
            sections.forEach(section => {
                section.classList.remove('profile__section--active');
                if (section.id === targetId) {
                    section.classList.add('profile__section--active');
                }
            });
        });
    });

    // Обработка изменения аватара
    const avatarInput = document.getElementById('avatar-upload');
    const avatarPreview = document.querySelector('.profile__user-avatar img');

    if (avatarInput && avatarPreview) {
        avatarInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    avatarPreview.src = e.target.result;
                    // Здесь можно добавить логику для отправки файла на сервер
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // Обработка переключателей в настройках
    const settingsToggles = document.querySelectorAll('.profile__settings-toggle input');
    settingsToggles.forEach(toggle => {
        toggle.addEventListener('change', function() {
            const setting = this.dataset.setting;
            const value = this.checked;

            // Сохраняем настройки в localStorage
            localStorage.setItem(`profile_setting_${setting}`, value);

            // Здесь можно добавить логику для отправки настроек на сервер
            console.log(`Setting "${setting}" changed to: ${value}`);
        });
    });

    // Обработка кнопок быстрых действий
    const actionButtons = document.querySelectorAll('.profile__action-card');
    actionButtons.forEach(button => {
        button.addEventListener('click', function() {
            const action = this.dataset.action;

            switch(action) {
                case 'edit-profile':
                    window.location.href = '/profile/edit';
                    break;
                case 'view-orders':
                    document.querySelector('[data-section="orders"]').click();
                    break;
                case 'view-favorites':
                    document.querySelector('[data-section="favorites"]').click();
                    break;
                case 'view-settings':
                    document.querySelector('[data-section="settings"]').click();
                    break;
            }
        });
    });

    // Загрузка сохраненных настроек при инициализации
    function loadSavedSettings() {
        settingsToggles.forEach(toggle => {
            const setting = toggle.dataset.setting;
            const savedValue = localStorage.getItem(`profile_setting_${setting}`);
            if (savedValue !== null) {
                toggle.checked = savedValue === 'true';
            }
        });
    }

    loadSavedSettings();
});
