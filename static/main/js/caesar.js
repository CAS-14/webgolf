function decipher() {
    var text = document.getElementById("inputtext").value.toLowercase();
    var alphabet = "abcdefghijklmnopqrstuvwxyz";

    document.getElementById("output_txt").innerHTML = "Loading..."

    var results = [];
    for (let offset = 1; offset < 26; offset++) {
        var comboSplit = [];
        for (let ind = 0; ind < text.length; ind++) {
            var currentChar = text[ind]

            if (alphabet.includes(currentChar)) {
                var newIndex = alphabet.indexOf(currentChar) + offset
                if (newIndex >= 26) { newIndex -= 26 }

                comboSplit.push(alphabet[newIndex]);
            } else {
                comboSplit.push(currentChar)
            }
        }

        console.log("Determined combination: "+comboSplit.join(""))
        results.push(comboSplit.join(""))
    }

    var allWords = "";
    var rawFile = new XMLHttpRequest();
    // words list from http://www.mieliestronk.com/corncob_lowercase.txt
    rawFile.open("GET", "https://www.weirdcease.com/tools/caesar/corncob_lowercase.txt", false);
    rawFile.onreadystatechange = function () {
        if(rawFile.readyState === 4) {
            if(rawFile.status === 200 || rawFile.status == 0) {
                allWords = rawFile.responseText;
            }
        }
    }
    rawFile.send(null);

    console.log("allWords first 20 chars: "+allWords.substring(0,20));

    var greatestCount = -1;
    var greatestIndex = -1;
    for (let i = 0; i < results.length; i++) {
        var count = 0;
        var resultWords = results[i].split(" ");

        for (let w = 0; w < resultWords.length; w++) {
            if (allWords.includes(resultWords[w])) { count++ }
        }

        if (count > greatestCount) {
            greatestCount = count;
            greatestIndex = i;
        }
    }

    console.log("greatestCount: "+greatestCount+"\ngreatestIndex: "+greatestIndex)

    var output = "";
    if (greatestIndex > -1) {
        output += "Most likely result:<br><br>"+results[greatestIndex];
        console.log(output);
        results.splice(greatestIndex, 1);
    } else {
        output += "No likely result could be found.";
    }

    output += "<br><br>All other combinations:"

    for (let r = 0; r < results.length; r++) {
        output += "<br><br>" + results[r];
    }

    document.getElementById("output_txt").innerHTML = output;

    if (document.getElementById("toggle_clear").checked) {
        clearbox();
    }
}

function clearbox() {
    document.getElementById("inputtext").value = "";
}