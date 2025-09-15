const background = document.querySelector('.background');

const cellSize = 280; // book spacing
const bookSize = 120; // book icon size

// RGB values (Red, Green, and Blue)
const colors = [
    "rgb(255, 0, 0)",
    "rgb(0, 255, 0)",
    "rgb(0, 0, 255)"
]; 

function fillBackground() {
    background.innerHTML = ""; // clearing old icons

    background.style.gridTemplateColumns = `repeat(auto-fill, ${cellSize}px)`;
    background.style.gridAutoRows = `${cellSize}px`;

    const cols = Math.ceil(window.innerWidth * 2 / cellSize);
    const rows = Math.ceil(window.innerHeight * 2 / cellSize);
    const total = cols * rows;

    for (let i = 0; i < total; i++) {
        const icon = document.createElement("i");
        icon.classList.add("fa-solid", "fa-book");
        icon.style.color = colors[i % colors.length];
        icon.style.fontSize = `${bookSize}px`;
        icon.style.transform = `rotate(${Math.random() * 90 - 45}deg)`
        background.appendChild(icon);
    }
}

fillBackground();

// If window resizes, fill the books in again
window.addEventListener("resize", fillBackground);