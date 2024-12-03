document.addEventListener("DOMContentLoaded", function() {
    const chatBox = document.getElementById("chat-box");
    
    // Auto-scroll to the bottom when the page loads or new messages are added
    chatBox.scrollTop = chatBox.scrollHeight;

    const chatForm = document.getElementById("chat-form");

    // Submit the form via Ajax to avoid page reload (Optional enhancement)
    chatForm.addEventListener("submit", function(e) {
        e.preventDefault();
        const queryInput = document.querySelector('.query-entry');
        const query = queryInput.value.trim();

        if (query !== "") {
            // Simulate appending the user's message to the chat
            const sentMessage = document.createElement("div");
            sentMessage.classList.add("message", "sent");
            sentMessage.innerHTML = `<div class="message-content">${query}</div>`;
            chatBox.appendChild(sentMessage);

            // Scroll to bottom
            chatBox.scrollTop = chatBox.scrollHeight;

            // Clear the input field
            queryInput.value = '';

            // Add a loading indicator (optional)
            const loadingIndicator = document.createElement("div");
            loadingIndicator.classList.add("message", "received");
            loadingIndicator.innerHTML = `<div class="message-content">...</div>`;
            chatBox.appendChild(loadingIndicator);

            // Simulate response after a delay (replace with actual API call)
            setTimeout(function() {
                chatBox.removeChild(loadingIndicator); // Remove loading
                const responseMessage = document.createElement("div");
                responseMessage.classList.add("message", "received");
                responseMessage.innerHTML = `<div class="message-content">{{new_answer}}</div>`;
                chatBox.appendChild(responseMessage);
                chatBox.scrollTop = chatBox.scrollHeight;
            }, 1000);
        }
    });
});