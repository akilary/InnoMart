document.addEventListener("DOMContentLoaded", () => {
    const toggleButtons = document.querySelectorAll(".auth__password-toggle");

    toggleButtons.forEach(button => {
        button.addEventListener("click", () => {
            const input = button.previousElementSibling;
            const icon = button.querySelector("span");
            
            if (input.type === "password") {
                input.type = "text";
                icon.textContent = "visibility";
            } else {
                input.type = "password";
                icon.textContent = "visibility_off";
            }
        });
    });
});
