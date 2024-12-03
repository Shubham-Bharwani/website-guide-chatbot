document.addEventListener('DOMContentLoaded', function () {
    const sendButton = document.getElementById('send-button');
    const userInput = document.getElementById('userInput');
    const messages = document.getElementById('messages');
    const modal = document.getElementById('modal');
    const submitModal = document.getElementById('submitModal');
    const modalInput = document.getElementById('modalInput');

    // Handle sending a message
    sendButton.addEventListener('click', function () {
        const userMessage = userInput.value.trim();

        if (userMessage) {
            appendMessage('user', userMessage); // Append user message
            userInput.value = ''; // Clear input field

            // Simulate a bot response after a short delay
            setTimeout(() => {
                appendMessage('bot', 'I am a bot!'); // Example bot response
            }, 1000);
        }
    });

    // Function to append messages
    function appendMessage(sender, message) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);
        messageDiv.textContent = message;
        messages.appendChild(messageDiv);
        messages.scrollTop = messages.scrollHeight; // Scroll to bottom
    }

    // Modal toggle
    submitModal.addEventListener('click', function () {
        const modalText = modalInput.value.trim();
        if (modalText) {
            alert('Modal info submitted: ' + modalText);
            modalInput.value = '';
            modal.style.display = 'none'; // Close the modal
        }
    });

    // Show modal on page load (for demonstration)
    setTimeout(() => {
        modal.style.display = 'flex'; // Show the modal after 2 seconds
    }, 2000);
});
