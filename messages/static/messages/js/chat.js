document.addEventListener("DOMContentLoaded", function() {
    const userId = {{ request.user.id }};  // Make sure you pass the user ID from your Django template
    const chatSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/chat/'
    );

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if (data.message) {
            // Handle incoming messages
            displayMessage(data.message);
        }
        if (data.send_receipt) {
            // Handle send receiptss
            displaySendReceipt(data.send_receipt);
        }
        if (data.read_receipt) {
            // Handle read receipt
            displayReadReceipt(data.read_receipt);
        }
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    document.querySelector('#chat-message-input').focus();
    document.querySelector('#chat-message-input').onkeyup = function(e) {
        if (e.keyCode === 13) {  // Enter key
            sendMessage();
        }
    };

    document.querySelector('#chat-message-submit').onclick = function(e) {
        sendMessage();
    };

    function sendMessage() {
        const messageInputDom = document.querySelector('#chat-message-input');
        const message = messageInputDom.value;
        chatSocket.send(JSON.stringify({
            'message': message,
            'sender': userId
        }));
        messageInputDom.value = '';
    }

    function displayMessage(message) {
        const messageList = document.querySelector('#message-list');
        const messageElement = document.createElement('li');
        messageElement.textContent = message.sender + ': ' + message.content;
        messageList.appendChild(messageElement);
    }

    function displaySendReceipt(receipt) {
        // Logic to display send receipt
    }

    function displayReadReceipt(receipt) {
        // Logic to display read receipt
    }
});
