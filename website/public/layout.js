const dropdown = document.getElementById("dropdown");
const dropdownText = document.getElementById("dropdown-text");

dropdown.addEventListener("mouseenter", () => {
    dropdownText.textContent = "Login ▴";
})
dropdown.addEventListener("mouseleave", () => {
    dropdownText.textContent = "Login ▾";
})