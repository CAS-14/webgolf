var colors = {
    "new-space": "#ff64ff",
    "new-stars": "#f6f5f2",
    "new-neon": "#85aae7",
    "new-fire-ice": "#f02c02",
    "omori-space": "#ff64ff",
    "omori-cranes": "#e0d2c2",
    "omori-forest": "#a2e0dA",
    "omori-firecity": "#f96412",
    "omori-water": "#b7cde5",
    "omori-dark": "#dddddd",
    "omori-faraway": "#bbd93f",
    "doge": "#cec59a", // secret dog 2012
}

var animations = [
    "none",
    "bob 1s infinite ease-in-out",
    "rainbow 1.5s infinite linear",
    "resize 1s infinite ease-in-out",
    "spin 1s infinite linear",
    "shake 0.3s infinite ease"
]

var themes = Object.keys(colors)
var public_theme_count = 4

function loadTheme() {
    var loaded = localStorage.getItem("theme")

    if (!(themes.includes(loaded))) {
        loaded = themes[0]
        localStorage.setItem("theme", loaded)
    }

    try {
        Array.from(document.getElementById("theme-select").options).forEach(function(optionElement) {
            optionElement.removeAttribute("selected")
        })
        document.getElementById("opt-"+loaded).setAttribute("selected", "")
    } catch {} 
    
    setTheme(loaded)
}

function selectTheme() { 
    var menu = document.getElementById("theme-select")
    var selected = menu.options[menu.selectedIndex].value
    localStorage.setItem("theme", selected)

    setTheme(selected)
}

function setTheme(theme) { 
    rs = document.querySelector(":root").style
    rs.setProperty("--accent", colors[theme])
    rs.setProperty("--background", "#000000 url('https://media.act25.com/themes/"+theme+".png')")
}

function randomTheme() {
    currentTheme = localStorage.getItem("theme")

    newTheme = currentTheme
    while (newTheme == currentTheme) {
        newTheme = themes[Math.floor((public_theme_count) * Math.random())]
    }

    localStorage.setItem("theme", newTheme)

    loadTheme()
}

function loadEffect() {
    var loaded = parseInt(localStorage.getItem("effect"))

    if (typeof animations[loaded] === "undefined") {
        loaded = 0
        localStorage.setItem("effect", loaded)
    }

    setEffect(loaded)
}

function setEffect(index) {
    rs = document.querySelector(":root").style
    rs.setProperty("--ascii-animation", animations[index])
}

function nextEffect() {
    var loaded = localStorage.getItem("effect")
    loaded ++

    if (typeof animations[loaded] === "undefined") {
        loaded = 0
    }

    localStorage.setItem("effect", loaded)

    loadEffect()
}

window.onload = function(){
    loadTheme()
    loadEffect()
}

function toggleItem(id) {
    var item = document.getElementById(id)
        
    if (item.style.display === "none" || item.style.display === "") {
        item.style.display = "block"
    } else {
        item.style.display = "none"
    }
}