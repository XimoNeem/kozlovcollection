document.addEventListener("DOMContentLoaded", function () {
    const sliderMain = document.querySelector(".slider-main");
    const slides = Array.from(document.querySelectorAll(".slide"));
    const thumbnailsContainer = document.querySelector(".slider-thumbnails");
    const originalThumbnails = Array.from(document.querySelectorAll(".thumbnail"));
    const prevBtn = document.querySelector(".prev");
    const nextBtn = document.querySelector(".next");

    const slideCount = slides.length;
    let currentIndex = 0;
    
    let isProgrammaticScroll = false;

    // Дублируем слайды, чтобы обеспечить бесшовность
    function cloneSlidesForLooping() {
        const fragmentStart = document.createDocumentFragment();
        const fragmentEnd = document.createDocumentFragment();

        slides.forEach((slide) => {
            const cloneStart = slide.cloneNode(true);
            cloneStart.classList.remove("active");
            fragmentEnd.appendChild(cloneStart);

            const cloneEnd = slide.cloneNode(true);
            cloneEnd.classList.remove("active");
            fragmentStart.appendChild(cloneEnd);
        });

        sliderMain.prepend(fragmentStart);
        sliderMain.append(fragmentEnd);
    }

    cloneSlidesForLooping();

    // Теперь нам нужно обновить список всех слайдов
    const allSlides = Array.from(document.querySelectorAll(".slide"));
    const visibleSlideCount = getVisibleSlideCount();

    // Устанавливаем стартовую прокрутку на "реальный" первый слайд
    const slideWidth = allSlides[0].offsetWidth;
    sliderMain.scrollLeft = slideWidth * slideCount;

    function getVisibleSlideCount() {
        const slide = allSlides[0];
        return Math.round(sliderMain.offsetWidth / slide.offsetWidth);
    }

    function scrollToIndex(index) {
        const targetIndex = index + slideCount;
        isProgrammaticScroll = true;

        sliderMain.scrollTo({
            left: targetIndex * slideWidth,
            behavior: "smooth",
        });

        // Сброс флага через таймер (время прокрутки ≈ 300ms)
        setTimeout(() => {
            isProgrammaticScroll = false;
        }, 350);
    }

    function getCircularIndex(index) {
        return (index + slideCount) % slideCount;
    }

    function updateActiveSlide(index) {
        allSlides.forEach((slide, i) => {
            const realIndex = i % slideCount;
            slide.classList.toggle("active", realIndex === index && Math.floor(i / slideCount) === 1);
        });
    
        originalThumbnails.forEach((thumb, i) => {
            thumb.classList.toggle("active", i === index);
        });
    }

    function updateThumbnails(index) {
        thumbnailsContainer.innerHTML = "";
    
        for (let i = 0; i < slideCount; i++) {
            const idx = getCircularIndex(index + i);
            const thumb = originalThumbnails[idx].cloneNode(true);
            thumb.classList.toggle("active", i === 0); // Активный — первый
            thumb.dataset.index = idx;
    
            thumb.addEventListener("click", () => {
                currentIndex = idx;
                scrollToIndex(currentIndex);
                updateActiveSlide(currentIndex);
                updateThumbnails(currentIndex);
            });
    
            thumbnailsContainer.appendChild(thumb);
        }
    }    

    function goToNext() {
        currentIndex = getCircularIndex(currentIndex + 1);
        scrollToIndex(currentIndex);
        updateActiveSlide(currentIndex);
        updateThumbnails(currentIndex);
    }

    function goToPrev() {
        currentIndex = getCircularIndex(currentIndex - 1);
        scrollToIndex(currentIndex);
        updateActiveSlide(currentIndex);
        updateThumbnails(currentIndex);
    }

    function correctLoopingScroll() {
        const maxScroll = slideWidth * (slideCount * 2);
        if (sliderMain.scrollLeft <= slideWidth * 0.5) {
            sliderMain.scrollLeft += slideCount * slideWidth;
        } else if (sliderMain.scrollLeft >= maxScroll - slideWidth * visibleSlideCount) {
            sliderMain.scrollLeft -= slideCount * slideWidth;
        }
    }

    // Инициализация
    scrollToIndex(currentIndex);
    updateActiveSlide(currentIndex);
    updateThumbnails(currentIndex);

    nextBtn?.addEventListener("click", goToNext);
    prevBtn?.addEventListener("click", goToPrev);

    originalThumbnails.forEach((thumb, idx) => {
        thumb.addEventListener("click", () => {
            currentIndex = idx;
            scrollToIndex(currentIndex);
            updateActiveSlide(currentIndex);
            updateThumbnails(currentIndex);
        });
    });

    // sliderMain.addEventListener("scroll", () => {
    //     if (!isProgrammaticScroll) {
    //         correctLoopingScroll();
    //     }
    // });

    window.addEventListener("resize", () => {
        scrollToIndex(currentIndex);
    });
});