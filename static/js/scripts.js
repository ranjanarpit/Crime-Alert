// // Smooth scrolling for navbar links
// document.querySelectorAll('.nav a').forEach(anchor => {
//     anchor.addEventListener('click', function(e) {
//         e.preventDefault();
//         const targetId = this.getAttribute('href').substring(1);
//         document.getElementById(targetId).scrollIntoView({
//             behavior: 'smooth'
//         });
//     });
// });

// // Initialize and add the map
// function initMap() {
//     // The location of Bihar Police Headquarters
//     const biharPoliceHQ = { lat: 25.612677, lng: 85.158875 };
//     // The map, centered at Bihar Police Headquarters
//     const map = new google.maps.Map(document.getElementById("map"), {
//         zoom: 15,
//         center: biharPoliceHQ,
//     });
//     // The marker, positioned at Bihar Police Headquarters
//     const marker = new google.maps.marker.AdvancedMarkerElement({
//         position: biharPoliceHQ,
//         map: map,
//         title: "Bihar Police Headquarters"
//     })
//     map.async = true;
// }

// // Load the map script once the page has loaded
// window.onload = loadMapScript;

// // slider
// const slides = document.querySelector('.slides');
// const totalSlides = document.querySelectorAll('.slide').length;

// let currentIndex = 0;

// function showNextSlide() {
//     currentIndex++;
//     if (currentIndex >= totalSlides) {
//         currentIndex = 0;
//     }
//     slides.style.transform = `translateX(-${currentIndex * 10}%)`; // Change to 10% per slide
// }

// setInterval(showNextSlide, 3000); // Change slide every 3 seconds

window.onload = function() {
    const slidesContainer = document.querySelector('.slides');
    const slideElements = document.querySelectorAll('.slide');

    // Clone the slides
    slideElements.forEach(slide => {
        let clone = slide.cloneNode(true);
        slidesContainer.appendChild(clone);
    });

    // Start continuous scrolling by setting animation state
    let scrollSpeed = 1;
    let scrollInterval;

    const startScrolling = () => {
        scrollInterval = setInterval(() => {
            slidesContainer.scrollLeft += scrollSpeed;
            // Reset to beginning when scrolled to the end
            if (slidesContainer.scrollLeft >= slidesContainer.scrollWidth / 2) {
                slidesContainer.scrollLeft = 0;
            }
        }, 10); // Controls the smoothness/speed of the scroll
    };

    startScrolling();

    // Pause scrolling on hover
    slidesContainer.addEventListener('mouseover', () => {
        clearInterval(scrollInterval);
    });

    // Resume scrolling when hover is removed
    slidesContainer.addEventListener('mouseout', () => {
        startScrolling();
    });
};