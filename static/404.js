const konamiCode = "ArrowUp,ArrowUp,ArrowDown,ArrowDown,ArrowLeft,ArrowRight,ArrowLeft,ArrowRight,b,a,Enter,";
var keysPressed = "";

document.onkeydown = (e) => {
    e = e || window.event;
    keysPressed = keysPressed + e.key + ",";

    if (keysPressed.includes(konamiCode)) {
        localStorage.setItem("theme", "doge");
        loadTheme();
        keysPressed = "";

        document.getElementById("visitMessage").innerHTML = "You have activated Doge mode!"
    }
}