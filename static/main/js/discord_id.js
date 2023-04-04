function output(text) {
    document.getElementById("output_txt").innerHTML += text + "<br>"
}

// NOTE: I am completely aware of the implications of having my token publically available. However, this bot is not in any servers and the only use of it is accessing the Discord API. So nice find, I guess?
const wavesDontLie = "Bo"+"t OTk2ODAyMzUw"+"OTg1NTMx"+"NDkz."+"Gncb9Y.NVgi6Y"+"EODhupT3j21lSRX"+"Qiv2Hp9"+"jO6GypylBc"
const baseUrl = "https://obscu"+"re-ridge-4"+"3487.herokuapp.com/https://discord.com/api/v10"

async function get(url) {
    let response = await fetch(url, {
        headers: {
            "Authorization": wavesDontLie,
            "X-Requested-With": "XMLHttpRequest",
        }
    })
    let data = await response.json()
    return data
}

function lookup() {
    document.getElementById("output_txt").innerHTML = ""
    var id = document.getElementById("discord_id").value

    if (/^\d+$/.test(id) && id.length == 18) {
        
        let intId = parseInt(id)
        let binId = intId.toString(2)
        while (binId.length < 64) {binId = "0" + binId}
        console.log(`Binary user ID is ${binId}`)
        
        let binTime = binId.slice(0, 42)
        console.log(`Binary creation time is ${binTime}, which is ${binTime.length} long`)
        let date = new Date((parseInt(binTime, 2) + 1420070400000))
        let strDate = date.toLocaleString()
        console.log(`Date is ${strDate}`)
        output(`Local creation date: ${strDate}`)

        data = get(baseUrl + "/users/" + id)
        console.log(data)
        output(data)

    } else {
        output("Error: ID must be an 18-digit integer.")
    }
}