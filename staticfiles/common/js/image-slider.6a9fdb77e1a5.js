document.addEventListener("DOMContentLoaded", function () {
    const sliderMain = document.querySelector(".slider-main");
    const slides = Array.from(document.querySelectorAll(".slide"));
    const thumbnailsContainer = document.querySelector(".slider-thumbnails");
    const thumbnails = Array.from(document.querySelectorAll(".thumbnail"));
    const prevBtn = document.querySelector(".prev");
    const nextBtn = document.querySelector(".next");

    const slideCount = slides.length;
    let currentIndex = 0;

    function scrollToSlide(index) {
        const slideWidth = slides[0].offsetWidth;
        sliderMain.scrollTo({
            left: index * slideWidth,
            behavior: "smooth",
        });
    }

    function updateActiveClasses(index) {
        slides.forEach((slide, i) => {
            slide.classList.toggle("active", i === index);
        });
        thumbnails.forEach((thumb, i) => {
            thumb.classList.toggle("active", i === index);
        });
    }

    function getCircularIndex(index) {
        return (index + slideCount) % slideCount;
    }

    function updateThumbnails(index) {
        thumbnailsContainer.innerHTML = ""; // Очищаем
    
        for (let i = 0; i < slideCount; i++) {
            const idx = getCircularIndex(index + i);
            const thumb = thumbnails[idx].cloneNode(true);
            thumb.classList.toggle("active", i === 0); // Активный теперь первый
            thumb.dataset.index = idx;
    
            thumb.addEventListener("click", () => {
                currentIndex = idx;
                scrollToSlide(currentIndex);
                updateActiveClasses(currentIndex);
                updateThumbnails(currentIndex);
            });
    
            thumbnailsContainer.appendChild(thumb);
        }
    }

    function goToNext() {
        currentIndex = getCircularIndex(currentIndex + 1);
        scrollToSlide(currentIndex);
        updateActiveClasses(currentIndex);
        updateThumbnails(currentIndex);
    }

    function goToPrev() {
        currentIndex = getCircularIndex(currentIndex - 1);
        scrollToSlide(currentIndex);
        updateActiveClasses(currentIndex);
        updateThumbnails(currentIndex);
    }

    // Стартовая инициализация
    scrollToSlide(currentIndex);
    updateActiveClasses(currentIndex);
    updateThumbnails(currentIndex);

    nextBtn?.addEventListener("click", goToNext);
    prevBtn?.addEventListener("click", goToPrev);

    thumbnails.forEach((thumb, idx) => {
        thumb.addEventListener("click", () => {
            currentIndex = idx;
            scrollToSlide(currentIndex);
            updateActiveClasses(currentIndex);
            updateThumbnails(currentIndex);
        });
    });

    // Обработка ресайза для корректной прокрутки
    window.addEventListener("resize", () => {
        scrollToSlide(currentIndex);
    });
});