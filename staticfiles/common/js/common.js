document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.getElementById("menuToggle");
    const closeMenu = document.getElementById("closeMenu");
    const sidebar = document.getElementById("kc-sidebar");
    const overlay = document.getElementById("kc-overlay");

    menuToggle.addEventListener("click", function () {
        sidebar.classList.add("open");
        overlay.classList.add("active");
    });

    closeMenu.addEventListener("click", function () {
        sidebar.classList.remove("open");
        overlay.classList.remove("active");
    });

    overlay.addEventListener("click", function () {
        sidebar.classList.remove("open");
        overlay.classList.remove("active");
    });
});