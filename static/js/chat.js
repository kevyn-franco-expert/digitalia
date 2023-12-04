document.addEventListener('DOMContentLoaded', (event) => {
    let ws;

    // Function to initialize WebSocket connection
    function connect() {
        // Construct WebSocket URL using the roomName from the Django template
        ws = new WebSocket('ws://localhost:8000/ws/chat/' + roomName + '/');

        // Event handler for receiving a message over WebSocket
        ws.onmessage = function (e) {
            var data = JSON.parse(e.data);
            displayMessage(data);
        };

        // Event handler for WebSocket closure
        ws.onclose = function (e) {
            console.error('Chat socket closed unexpectedly');
            // Attempt to reconnect after a short delay
            setTimeout(function () {
                connect();
            }, 1000);
        };
    }

    // Function to send a message over WebSocket
    function sendMessage(message) {
        if (ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({'message': message}));
        } else {
            console.error('WebSocket is not open. Unable to send message.');
        }
    }

    // Function to display a message in the chat box
    function displayMessage(data) {
        var chatBox = document.getElementById('chatBox');
        const userColor = stringToColor(data.user);
        var formattedMessage = `<div><b style="color: ${userColor};">${data.user}:</b> ${data.message}</div>`;
        chatBox.innerHTML += formattedMessage;
        // Auto-scroll to the latest message
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Add event listener for the message form
    document.getElementById('messageForm').addEventListener('submit', function (e) {
        e.preventDefault();
        let messageInput = document.getElementById('messageInput');
        let message = messageInput.value;
        sendMessage(message);
        messageInput.value = ''; // Clear the input field
    });

    document.getElementById('return_id').addEventListener('click', function () {
        window.location.href = '/room/';
    });

    connect(); // Initialize WebSocket connection

    function stringToColor(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            hash = str.charCodeAt(i) + ((hash << 5) - hash);
        }

        let color = '#';
        for (let i = 0; i < 3; i++) {
            const value = (hash >> (i * 8)) & 0xFF;
            color += ('00' + value.toString(16)).substr(-2);
        }
        return color;
    }
});
