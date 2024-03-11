function multiSlideCarousel(vmwCarousel) {
    const outerCarousel = vmwCarousel.querySelector('.outer-carousel');
    const carousel = outerCarousel.querySelector('.middle-carousel');
    const carouselTrack = outerCarousel.querySelector('.inner-carousel')
    const slides = carousel.querySelectorAll('vmw-carousel-item');

    const prevBtn = outerCarousel.querySelector('.navigation-arrow.left-arrow > button');
    const nextBtn = outerCarousel.querySelector('.navigation-arrow.right-arrow > button');
    const carouselNav = vmwCarousel.querySelector('.navigation > .navigation-slide-button-container');

    const totalSlides = slides.length;

    let slideWidth = 0;
    let numVisibleSlides = 0;
    let currentIndex = 0;
    let numSlideGroups = 0;
    let slideMoveDistance = 0;

    prevBtn.addEventListener('click', showPreviousSlides);
    nextBtn.addEventListener('click', showNextSlides);

    function updateCarousel() {
        slideWidth = slides[0].offsetWidth;
        numVisibleSlides = Math.round(outerCarousel.offsetWidth / slideWidth);
        if(numVisibleSlides < 1) {
            numVisibleSlides = 1;
        }
        numSlideGroups = Math.ceil(totalSlides / numVisibleSlides);
        slideMoveDistance = numVisibleSlides * slideWidth;
        addNavSlideButtons();
        showSlide(0);
        if (totalSlides > numVisibleSlides){
            prevBtn.style.display = nextBtn.style.display = carouselNav.style.display = "flex"
        }else{
            prevBtn.style.display = nextBtn.style.display = carouselNav.style.display = "none"
        }

        updateVisibleSlides(0);
    }

    function showPreviousSlides() {
        if (currentIndex - numVisibleSlides < 0) {
            let lastPageElements = totalSlides % numVisibleSlides;
            if (lastPageElements === 0){
                lastPageElements = numVisibleSlides
            }

            currentIndex = totalSlides - lastPageElements;
        } else {
            currentIndex -= numVisibleSlides;
        }
        carouselTrack.style.transform = `translateX(-${currentIndex * slideWidth}px)`;
        updateNavSlideButtons(Math.ceil(currentIndex / numVisibleSlides));
        updateVisibleSlides(currentIndex);
    }

    function showNextSlides() {
        if (currentIndex > totalSlides - numVisibleSlides - 1) {
            currentIndex = 0;
        } else {
            currentIndex += numVisibleSlides;

        }
        carouselTrack.style.transform = `translateX(-${currentIndex * slideWidth}px)`;
        updateNavSlideButtons(Math.ceil(currentIndex / numVisibleSlides));
        updateVisibleSlides(currentIndex);
    }

    function addNavSlideButtons() {
        carouselNav.innerHTML = '';

        const svgHtml = `
    <svg viewBox="0 0 36 36" xmlns="http://www.w3.org/2000/svg" fill="currentColor" aria-hidden="true">
      <path d="M18,34A16,16,0,1,1,34,18,16,16,0,0,1,18,34Z"></path>
    </svg>
    `;

        for (let i = 0; i < numSlideGroups; i++) {
            if (!isFinite(numSlideGroups)) {
                break;
            }

            const button = document.createElement('button');
            button.classList.add('btn', 'btn-sm', 'btn-link', 'btn-icon');
            button.setAttribute('slide-index', i);
            button.innerHTML = svgHtml;

            if (i === currentIndex) {
                button.classList.add('active');
            }

            button.addEventListener('click', function () {
                const slideIndex = parseInt(this.getAttribute('slide-index'));
                showSlide(slideIndex);
            });

            carouselNav.appendChild(button);
        }

    }

    function showSlide(index) {
        currentIndex = (index * numVisibleSlides) - numVisibleSlides;
        showNextSlides();
    }

    function updateNavSlideButtons(index) {
        currentNavBtn = carouselNav.querySelector('.active');
        if (currentNavBtn) {
            currentNavBtn.classList.remove('active');
        }
        newNavBtn = carouselNav.querySelector(`[slide-index="${index}"]`);
        newNavBtn.classList.add('active');
    }

    function updateVisibleSlides(currentIndex) {
        // Remove the inactive class for all slides that should be visible.
        for (let i = currentIndex; i < currentIndex + numVisibleSlides; i++) {
            if (i < totalSlides && slides[i].classList.contains('inactive')) {
                slides[i].classList.remove('inactive');
            }
        }

        // Add the inactive class for all slides that should not be visible.
        for (let i = 0; i < currentIndex; i++) {
            if (!slides[i].classList.contains('inactive')) {
                slides[i].classList.add('inactive');
            }
        }

        // Add the inactive class for all slides that should not be visible.
        for (let i = currentIndex + numVisibleSlides; i < totalSlides; i++) {
            if (!slides[i].classList.contains('inactive')) {
                slides[i].classList.add('inactive');
            }
        }
    }

    window.addEventListener('resize', updateCarousel);
    updateCarousel();
}

function handleAllCarousels() {
    const carousels = document.querySelectorAll('vmw-carousel');

    carousels.forEach(function (carousel) {
        multiSlideCarousel(carousel);
    });
}

const hamburgerBtn = document.querySelector(".header-hamburger-trigger");
const drawer = document.querySelector(".nav-drawer");
const closeBtn = drawer.querySelector('.close-btn');

function addNavLinksToDrawer() {
    const headerNav = document.querySelector('.header-nav');
    const headerNavClone = headerNav.cloneNode(true)
    const navLinks = headerNavClone.querySelectorAll('.nav-link');
    const drawerNav = document.createElement("ul");

    navLinks.forEach((navLink) => {
        const listItem = document.createElement("li");
        listItem.appendChild(navLink);
        drawerNav.appendChild(listItem);
    })
    drawer.appendChild(drawerNav)
}

function closeDrawer(){
    drawer.classList.remove('active');
}

hamburgerBtn.addEventListener("click", () => {
    drawer.classList.toggle("active");
});

document.addEventListener("click", (e) => {
    if (e.target !== drawer && e.target !== hamburgerBtn && !drawer.contains(e.target)) {
        closeDrawer()
    }
});
closeBtn.addEventListener('click', closeDrawer);

document.addEventListener('DOMContentLoaded', handleAllCarousels);
document.addEventListener('DOMContentLoaded', addNavLinksToDrawer);
