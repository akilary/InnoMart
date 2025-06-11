/** Показывает уведомление пользователю */
export function showNotification(message, type = "info", duration = 1500) {
    let notificationContainer = document.querySelector(".notifications");

    if (!notificationContainer) {
        notificationContainer = document.createElement("div");
        notificationContainer.className = "notifications";
        document.body.appendChild(notificationContainer);
    }

    let icon;
    switch (type) {
        case "success":
            icon = "check_circle";
            break;
        case "error":
            icon = "error";
            break;
        case "warning":
            icon = "warning";
            break;
        case "info":
        default:
            icon = "info";
            break;
    }

    const notification = document.createElement("div");
    notification.className = `notification notification--${type}`;
    notification.innerHTML = `
        <div class="notification__content">
            <span class="material-icons notification__icon">${icon}</span>
            <span class="notification__message">${message}</span>
        </div>
        <button class="notification__close" aria-label="Закрыть">&times;</button>
    `;

    notificationContainer.appendChild(notification);

    const closeBtn = notification.querySelector(".notification__close");
    closeBtn.addEventListener("click", () => {
        notification.classList.add("notification--closing");
        setTimeout(() => {
            notification.remove();
        }, 300);
    });

    setTimeout(() => {
        notification.classList.add("notification--closing");
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, duration);

    return notification;
}
