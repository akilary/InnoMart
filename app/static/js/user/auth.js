document.addEventListener("DOMContentLoaded", () => {
    setupPasswordToggle();
});

/* Переключение видимости пароля */
function setupPasswordToggle() {
    document.querySelectorAll(".auth__password-toggle").forEach(button => {
        button.addEventListener("click", () => {
            const input = button.previousElementSibling;
            const icon = button.querySelector("span");
            const isPassword = input.type === "password";

            input.type = isPassword ? "text" : "password";
            icon.textContent = isPassword ? "visibility" : "visibility_off";
        });
    });
}
