var currentIndex = 0;
var images = [];

function openModal(newImages, index, isWhiteBackground = false) {
    images = newImages;
    currentIndex = index;

    const modal = document.getElementById("imageModal");
    const modalImg = document.getElementById("modalImage");

    modal.classList.remove("hidden");
    document.body.classList.add("no-scroll");

    modalImg.src = images[currentIndex];
    modalImg.classList.remove("fullscreen");

    // Добавляем класс для белого фона, если передан флаг
    if (isWhiteBackground) {
        modal.classList.add("white-background");
    } else {
        modal.classList.remove("white-background");
    }

    const svgImages = modal.querySelectorAll(".image-modal-image");
    svgImages.forEach(img => {
        if (isWhiteBackground) {
            img.style.filter = "invert(1)";
        } else {
            img.style.filter = "";
        }
    });
}

function closeModal() {
    const modal = document.getElementById("imageModal");
    const modalImg = document.getElementById("modalImage");

    modal.classList.add("hidden");
    document.body.classList.remove("no-scroll");

    exitFullscreen();
    modalImg.classList.remove("fullscreen");
}

function changeImage(direction) {
    const modalImg = document.getElementById("modalImage");

    currentIndex += direction;
    if (currentIndex < 0) {
        currentIndex = images.length - 1;
    } else if (currentIndex >= images.length) {
        currentIndex = 0;
    }

    // Обновить изображение
    modalImg.classList.remove("fullscreen");
    modalImg.src = images[currentIndex];

    // Если находимся в fullscreen — заново применяем класс
    if (document.fullscreenElement) {
        // Подождем, пока картинка подгрузится, чтобы зум работал нормально
        modalImg.onload = () => {
            modalImg.classList.add("fullscreen");
        };
    }
}

// Полноэкран по клику
document.addEventListener("DOMContentLoaded", function () {
    const modalImg = document.getElementById("modalImage");

    modalImg.addEventListener("click", function () {
        if (!document.fullscreenElement) {
            enterFullscreen(modalImg);
            modalImg.classList.add("fullscreen");
        } else {
            exitFullscreen();
            modalImg.classList.remove("fullscreen");
        }
    });

    // Обработка стрелок с клавиатуры (← и →)
    document.addEventListener("keydown", function (e) {
        if (!document.getElementById("imageModal").classList.contains("hidden")) {
            if (e.key === "ArrowLeft") {
                changeImage(-1);
            } else if (e.key === "ArrowRight") {
                changeImage(1);
            } else if (e.key === "Escape") {
                closeModal();
            }
        }
    });
});

function enterFullscreen(element) {
    if (element.requestFullscreen) {
        element.requestFullscreen();
    } else if (element.webkitRequestFullscreen) {
        element.webkitRequestFullscreen();
    } else if (element.msRequestFullscreen) {
        element.msRequestFullscreen();
    }
}

function exitFullscreen() {
    if (document.exitFullscreen) {
        document.exitFullscreen();
    } else if (document.webkitExitFullscreen) {
        document.webkitExitFullscreen();
    } else if (document.msExitFullscreen) {
        document.msExitFullscreen();
    }
}
