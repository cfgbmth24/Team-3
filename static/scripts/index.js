document.addEventListener("DOMContentLoaded", function() {
    const track = document.querySelector(".carousel-track");
    const slides = document.querySelectorAll(".carousel-slide");
    const prevButton = document.querySelector(".prev-button");
    const nextButton = document.querySelector(".next-button");
    const slideWidth = slides[0].offsetWidth;

    let currentIndex = 0;

    prevButton.addEventListener("click", () => {
        currentIndex = (currentIndex - 1 + slides.length) % slides.length;
        updateCarousel();
    });

    nextButton.addEventListener("click", () => {
        currentIndex = (currentIndex + 1) % slides.length;
        updateCarousel();
    });

    function updateCarousel() {
        const offset = -currentIndex * slideWidth;
        track.style.transform = `translateX(${offset}px)`;
    }
});
