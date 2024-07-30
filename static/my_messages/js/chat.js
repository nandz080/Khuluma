document.addEventListener("DOMContentLoaded", function() {
    const userId = {{ request.user.id }};  // Corrected syntax

    const roomName = JSON.parse(document.getElementById('room-name').textContent);
    const chatSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
    );

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        displayMessage(data);
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    document.querySelector('#chat-message-input').focus();
    document.querySelector('#chat-message-input').onkeyup = function(e) {
        if (e.keyCode === 13) {  // Enter key
            document.querySelector('#chat-message-submit').click();
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
        const messageElement = document.querySelector(`#message-${receipt.message_id}`);
        if (messageElement) {
            messageElement.classList.add('sent');
        }
    }

    function displayReadReceipt(receipt) {
        const messageElement = document.querySelector(`#message-${receipt.message_id}`);
        if (messageElement) {
            messageElement.classList.add('read');
        }
    }
});
