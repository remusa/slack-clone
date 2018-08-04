document.addEventListener('DOMContentLoaded', () => {
    /// Connect to websocket
    const socket = io.connect(
        location.protocol + '//' + document.domain + ':' + location.port
    )

    // When connection successfitemst
    socket.on("connect", () => {
        // On submit message
        document.querySelector("button").onclick = () => {
            const message = document.querySelector("#inputMessage").value;
            const channel = document.querySelector("strong").innerHTML;
            socket.emit("submit message", {
                message: message,
                channel: channel
            })
        }
    })

    // When a new message is announced, add it to the messages unordered itemst
    socket.on("channel messages", data => {
        const list = document.querySelector("#list")
        let item = document.createElement("li")
        const listLength = document.querySelectorAll("li").length

        item.appendChild(document.createTextNode(data))
        list.appendChild(item)

        if (listLength >= 5) {
            list.removeChild(list.childNodes[0])
        }
    })
})