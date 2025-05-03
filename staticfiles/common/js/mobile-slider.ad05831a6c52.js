document.addEventListener("DOMContentLoaded", function () {
    const slider = document.querySelector(".kc-mobile-slider");
    const slides = document.querySelectorAll(".kc-mobile-slider-slide");

    const dots = document.querySelectorAll(".kc-mobile-slider-dot");

    let currentIndex = 0;
    let startX = 0;
    let isSwiping = false;
    
    function updateSlider() {
        slider.style.transform = `translateX(-${currentIndex * 100}%)`;
    
        const defaultColor = "#1E8DD3";
        const activeColor = slider.dataset.color ? slider.dataset.color : defaultColor;
    
        dots.forEach((dot, index) => {
            const isActive = index === currentIndex;
            dot.classList.toggle("active", isActive);
            dot.style.backgroundColor = isActive ? activeColor : "#ccc";
        });
    }
    

    function nextSlide() {
        if (currentIndex < slides.length - 1) {
            currentIndex++;
        } else {
            currentIndex = 0; // Зацикливание
        }
        updateSlider();
    }

    function prevSlide() {
        if (currentIndex > 0) {
            currentIndex--;
        } else {
            currentIndex = slides.length - 1; // Зацикливание
        }
        updateSlider();
    }


    // Добавляем обработку клика по индикаторам
    dots.forEach((dot, index) => {
        dot.addEventListener("click", () => {
            currentIndex = index;
            updateSlider();
        });
    });

    // Обработчик свайпа
    slider.addEventListener("touchstart", (e) => {
        startX = e.touches[0].clientX;
        isSwiping = true;
    });

    slider.addEventListener("touchmove", (e) => {
        if (!isSwiping) return;
        let diff = e.touches[0].clientX - startX;
        if (diff > 50) {
            prevSlide();
            isSwiping = false;
        } else if (diff < -50) {
            nextSlide();
            isSwiping = false;
        }
    });

    slider.addEventListener("touchend", () => {
        isSwiping = false;
    });

    updateSlider(); // Инициализация
});
