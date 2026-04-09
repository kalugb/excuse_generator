window.onload = () => {
    const transitions = document.querySelectorAll(".global-pretransition");
    
    transitions.forEach(el => {
        el.classList.remove("global-pretransition");
    });
};

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

const situationInput = document.getElementById("situation");

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

generateBtn.addEventListener("click", async () => {
    // reset
    if (!postGenerate.classList.contains("hidden")) {
        postGenerate.classList.add("hidden");
    }
    const paragraphs = document.querySelectorAll("#post-generate p");
    paragraphs.forEach((p, index) => {
        p.textContent = `Excuse ${index + 1}: `;
    })

    input = situationInput.value;
    if (input === "") {
        throw new Error("Please enter a situation");
    } 

    const payload = {
        situation: input,
        context: contextSymbol,
        seriousness: seriousSymbol,
        length: lengthSymbol,
    };

    inGenerate.classList.toggle("hidden");
    generateBtn.classList.toggle("hidden");

    try {
        const res = await fetch("/generateExcuse", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });
        const result = await res.json();
        console.log(result)

        postGenerate.classList.remove("hidden");
        inGenerate.classList.toggle("hidden");
        generateBtn.classList.toggle("hidden");

        result.forEach((text, index) => {
            paragraphs[index].textContent += text;
        });

    } catch (err) {
        console.error(err);
    }
});