document.addEventListener('DOMContentLoaded', () => {
    /// Connect to websocket
    const socket = io.connect(
        location.protocol + '//' + document.domain + ':' + location.port
    )

    // When connection success
    socket.on("connect", () => {
        // On submit message
        document.querySelector("button").onclick = () => {
            const message = document.querySelector("#inputMessage").value;
            const channel = document.querySelector("strong").innerHTML;
            socket.emit("submit message", {
                message: message,
                channel: channel
            })

            const list = document.querySelector("#list")
            let listLength = list.querySelectorAll("li").length
            if (listLength >= 5) {
                list.removeChild(list.firstChild) //childNodes[0]
            }

            document.querySelector("#inputMessage").value = ""
        }
    })

    // When a new message is announced, add new messages to the messages unordered list
    socket.on("channel messages", data => {
        const list = document.querySelector("#list")
        const item = document.createElement('li');
        item.innerHTML = data;
        // item.appendChild(document.createTextNode(data))
        list.appendChild(item)
    })
})