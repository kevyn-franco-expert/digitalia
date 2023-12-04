document.querySelector('#joinChatForm form').addEventListener('submit', function (e) {
    e.preventDefault();
    var chatId = document.getElementById('chatId').value;
    window.location.href = `/message/${chatId}/`;  // Redirect to chat room
});