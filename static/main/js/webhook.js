function send() {
    const request = new XMLHttpRequest();
    request.open("POST", document.getElementById("webhook_url").value);
    request.setRequestHeader('Content-type', 'application/json');
    const params = {content: document.getElementById("message").value}
    request.send(JSON.stringify(params));

    if (document.getElementById("toggle_clear").checked) {
        clearbox();
    }
}

function clearbox() {
    document.getElementById("message").value = "";
}