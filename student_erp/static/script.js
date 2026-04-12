/* News Slider */
let slides = document.querySelectorAll(".slide");
let index = 0;

setInterval(() => {
    slides[index].classList.remove("active");
    index = (index + 1) % slides.length;
    slides[index].classList.add("active");
}, 3000);

/* Gallery Slider */
let gslides = document.querySelectorAll(".gslide");
let gindex = 0;

setInterval(() => {
    gslides[gindex].classList.remove("active");
    gindex = (gindex + 1) % gslides.length;
    gslides[gindex].classList.add("active");
}, 3500);
function toggleTheme() {
    document.body.classList.toggle("dark");
}
