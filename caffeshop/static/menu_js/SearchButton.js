// In the name of GOD
const searchBtn = document.querySelector(".search-btn");
const searchBox = document.querySelector(".search-box");
const searchInput = searchBox.querySelector(".input");

searchBtn.onclick = () => {
    searchBox.classList.toggle("active");
    searchBtn.classList.toggle("active");
    const searchIcon = searchBtn.querySelector(".bi-search");
    const clockIcon = searchBtn.querySelector(".bi-x-lg");

    if (searchInput.type == 'hidden') {
        searchInput.type = 'search'
    } else {
        searchInput.type = 'hidden'
    }
    searchIcon.classList.toggle("d-none");
    clockIcon.classList.toggle("d-none");

}