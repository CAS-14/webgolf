var current = "i'm a dog"

function expand(image) {
    try { current.remove() } catch { console.log("didn't hide thing") }

    let gallery = image.parentNode.parentNode.parentNode
    let nextRow = image.parentNode.parentNode.nextSibling

    let expandedImage = document.createElement("img")
    expandedImage.classList.add("expand")
    expandedImage.src = image.src
    expandedImage.onclick = function () { current.remove() }

    let expandedItem = document.createElement("div")
    expandedItem.appendChild(expandedImage)

    let expandedRow = document.createElement("div")
    expandedRow.classList.add("gallery-row")
    expandedRow.appendChild(expandedItem)

    gallery.insertBefore(expandedRow, nextRow)
    expandedRow.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'start' })
    current = expandedRow
}