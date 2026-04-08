window.onload = () => {
    const transitions = document.querySelectorAll(".global-pretransition");
    
    transitions.forEach(el => {
        el.classList.remove("global-pretransition");
    });
};

console.log("test");