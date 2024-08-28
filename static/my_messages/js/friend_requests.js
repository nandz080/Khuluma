document.addEventListener('DOMContentLoaded', function() {
    // Event listener for Add Friend buttons
    document.querySelectorAll('.btn-add').forEach(function(button) {
        button.addEventListener('click', function() {
            const friendId = this.getAttribute('data-friend-id');
            addFriend(friendId);
        });
    });

    // Event listener for Remove Friend buttons
    document.querySelectorAll('.btn-remove').forEach(function(button) {
        button.addEventListener('click', function() {
            const friendId = this.getAttribute('data-friend-id');
            removeFriend(friendId);
        });
    });

    // Event listener for Cancel buttons
    document.querySelectorAll('.btn-cancel').forEach(function(button) {
        button.addEventListener('click', function() {
            const friendId = this.getAttribute('data-friend-id');
            cancelRequest(friendId);
        });
    });
});

function addFriend(friendId) {
    console.log(`Add friend with ID: ${friendId}`);
    // Disable the Add Friend button and show the Cancel button
    document.querySelector(`#friend-${friendId} .btn-add`).disabled = true;
    document.querySelector(`#friend-${friendId} .btn-cancel`).style.display = 'inline-block';

    // You can add an AJAX request here to send the friend request to the server
}

function removeFriend(friendId) {
    console.log(`Remove friend with ID: ${friendId}`);
    // Implement your remove friend logic here

    // You can add an AJAX request here to remove the friend on the server
}

function cancelRequest(friendId) {
    console.log(`Cancel friend request for ID: ${friendId}`);
    // Re-enable the Add Friend button and hide the Cancel button
    document.querySelector(`#friend-${friendId} .btn-add`).disabled = false;
    document.querySelector(`#friend-${friendId} .btn-cancel`).style.display = 'none';

    // You can add an AJAX request here to cancel the friend request on the server
}
