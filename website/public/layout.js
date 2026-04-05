const dropdown = document.getElementById("dropdown");
const dropdownText = document.getElementById("dropdown-text");

const generateBtn = document.getElementById("generate-btn");
const btnContainer = document.getElementById("btn-container");
const inGenerate = document.getElementById("in-generate");
const postGenerate = document.getElementById("post-generate");

const context = document.querySelectorAll(".context-menu");
const serious = document.querySelectorAll(".serious-menu");
const length = document.querySelectorAll(".length-menu");
const selectedContext = document.querySelector(".context-menu.selected");
const selectedSerious = document.querySelector(".serious-menu.selected");
const selectedLength = document.querySelector(".length-menu.selected");
let contextSymbol = "general", seriousSymbol = "serious", lengthSymbol = "short"

dropdown.addEventListener("mouseenter", () => {
    dropdownText.textContent = "Login ▴";
})
dropdown.addEventListener("mouseleave", () => {
    dropdownText.textContent = "Login ▾";
})

generateBtn.addEventListener("click", () => {
    inGenerate.classList.toggle("hidden");
    postGenerate.classList.toggle("hidden");
})

context.forEach((item) => {
    item.addEventListener("click", () => {
        context.forEach((item) => {
            item.classList.remove("selected");
        })
        item.classList.add("selected");
        contextSymbol = item.getAttribute("data-symbol");
    })
})

serious.forEach((item) => {
    item.addEventListener("click", () => {
        serious.forEach((item) => {
            item.classList.remove("selected");
        })
        item.classList.add("selected");
        seriousSymbol = item.getAttribute("data-symbol");
    })
})

length.forEach((item) => {
    item.addEventListener("click", () => {
        length.forEach((item) => {
            item.classList.remove("selected");
        })
        item.classList.add("selected");
        lengthSymbol = item.getAttribute("data-symbol");
    })
})