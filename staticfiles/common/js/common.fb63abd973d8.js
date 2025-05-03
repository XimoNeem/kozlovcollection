document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.getElementById("menuToggle");
    const closeMenu = document.getElementById("closeMenu");
    const sidebar = document.getElementById("kc-sidebar");
    const overlay = document.getElementById("kc-overlay");

    menuToggle.addEventListener("click", function () {
        sidebar.classList.add("open");
        overlay.classList.add("active");
    });

    if (closeMenu) {
        closeMenu.addEventListener("click", function () {
            if (sidebar && overlay) {
                sidebar.classList.remove("open");
                overlay.classList.remove("active");
            }
        });
    }

    overlay.addEventListener("click", function () {
        sidebar.classList.remove("open");
        overlay.classList.remove("active");
    });

    document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") {
            if (sidebar.classList.contains("open")) {
                // Закрываем меню, если оно открыто
                sidebar.classList.remove("open");
                overlay.classList.remove("active");
            } else {
                // Открываем меню, если оно закрыто
                sidebar.classList.add("open");
                overlay.classList.add("active");
            }
        }
    });

});