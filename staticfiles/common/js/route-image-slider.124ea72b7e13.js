document.addEventListener("DOMContentLoaded", function () {
    let slides = document.querySelectorAll(".slide");
    let thumbnails = document.querySelectorAll(".thumbnail");
    let dots = document.querySelectorAll(".dot");
    let prevBtn = document.querySelector(".prev");
    let nextBtn = document.querySelector(".next");

    let desktop_second_preview = document.querySelector(".second-preview");

    let currentIndex = 0;

    function updateSlider(index) {
        desktop_second_preview.classList.toggle("active", currentIndex + 1);

        slides.forEach((slide, i) => {
            slide.classList.toggle("active", i === index);
        });
        thumbnails.forEach((thumb, i) => {
            thumb.classList.toggle("active", i === index);
        });
        dots.forEach((dot, i) => {
            dot.classList.toggle("active", i === index);
        });
    }

    nextBtn.addEventListener("click", function () {
        currentIndex = (currentIndex + 1) % slides.length;
        updateSlider(currentIndex);
    });

    prevBtn.addEventListener("click", function () {
        currentIndex = (currentIndex - 1 + slides.length) % slides.length;
        updateSlider(currentIndex);
    });

    thumbnails.forEach((thumb, index) => {
        thumb.addEventListener("click", function () {
            currentIndex = index;
            updateSlider(currentIndex);
        });
    });

    dots.forEach((dot, index) => {
        dot.addEventListener("click", function () {
            currentIndex = index;
            updateSlider(currentIndex);
        });
    });
});
