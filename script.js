const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const chatMessages = document.getElementById('chatMessages');
const approvalModal = document.getElementById('approvalModal');
const approvalMessage = document.getElementById('approvalMessage');
const approveBtn = document.getElementById('approveBtn');
const denyBtn = document.getElementById('denyBtn');

// Store current approval ID
let currentApprovalId = null;

// Viewport height fix for mobile browsers
function setViewportHeight() {
    const vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
}

setViewportHeight();
window.addEventListener('resize', setViewportHeight);

function addMessage(text, isUser) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;

    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.textContent = text;

    messageDiv.appendChild(messageContent);
    chatMessages.appendChild(messageDiv);

    scrollToBottom();
}

function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function sendMessage() {
    const message = messageInput.value.trim();

    if (message === '') {
        return;
    }

    // Show user message
    addMessage(message, true);
    messageInput.value = '';

    // Disable input while waiting for response
    messageInput.disabled = true;
    sendButton.disabled = true;
    sendButton.textContent = 'Sending...';

    // Send message to backend
    fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            message: message
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.needs_approval) {
            // Tool needs approval! Show modal
            showApprovalModal(data.approval_id, data.tool_name, data.tool_args);
        } else if (data.response) {
            // Normal response
            addMessage(data.response, false);
            // Re-enable input
            messageInput.disabled = false;
            sendButton.disabled = false;
            sendButton.textContent = 'Send';
            messageInput.focus();
        } else if (data.error) {
            addMessage('Error: ' + data.error, false);
            // Re-enable input
            messageInput.disabled = false;
            sendButton.disabled = false;
            sendButton.textContent = 'Send';
            messageInput.focus();
        }
    })
    .catch(error => {
        addMessage('Error connecting to server: ' + error.message, false);
        // Re-enable input
        messageInput.disabled = false;
        sendButton.disabled = false;
        sendButton.textContent = 'Send';
        messageInput.focus();
    });
}

sendButton.addEventListener('click', sendMessage);

messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// ============================================
// APPROVAL MODAL FUNCTIONS
// ============================================

function showApprovalModal(approvalId, toolName, toolArgs) {
    currentApprovalId = approvalId;

    // Format the tool arguments nicely
    const argsText = Object.entries(toolArgs)
        .map(([key, value]) => `${key}: "${value}"`)
        .join(', ');

    approvalMessage.textContent = `Agent wants to call '${toolName}' with arguments: ${argsText}`;
    approvalModal.classList.add('show');
}

function hideApprovalModal() {
    approvalModal.classList.remove('show');
    currentApprovalId = null;
}

function handleApproval(approved) {
    if (!currentApprovalId) return;

    // Disable buttons while processing
    approveBtn.disabled = true;
    denyBtn.disabled = true;
    approveBtn.textContent = 'Processing...';

    // Send approval decision to backend
    fetch('http://localhost:5000/approve', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            approval_id: currentApprovalId,
            approved: approved
        })
    })
    .then(response => response.json())
    .then(data => {
        // Hide modal
        hideApprovalModal();

        // Show bot response
        if (data.response) {
            addMessage(data.response, false);
        } else if (data.error) {
            addMessage('Error: ' + data.error, false);
        }

        // Re-enable input
        messageInput.disabled = false;
        sendButton.disabled = false;
        sendButton.textContent = 'Send';
        messageInput.focus();

        // Reset button states
        approveBtn.disabled = false;
        denyBtn.disabled = false;
        approveBtn.textContent = 'Approve';
    })
    .catch(error => {
        hideApprovalModal();
        addMessage('Error: ' + error.message, false);

        // Re-enable input
        messageInput.disabled = false;
        sendButton.disabled = false;
        sendButton.textContent = 'Send';
        messageInput.focus();

        // Reset button states
        approveBtn.disabled = false;
        denyBtn.disabled = false;
        approveBtn.textContent = 'Approve';
    });
}

// Approve button click
approveBtn.addEventListener('click', () => {
    handleApproval(true);
});

// Deny button click
denyBtn.addEventListener('click', () => {
    handleApproval(false);
});
