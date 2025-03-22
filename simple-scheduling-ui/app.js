// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const messageForm = document.getElementById('messageForm');
const userMessageInput = document.getElementById('userMessage');

// API URL (Flask server)
const API_URL = 'http://localhost:5001/api/chat';

// Initial loading state
let isWaitingForResponse = false;

// Add event listener for form submission
messageForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const message = userMessageInput.value.trim();
    if (!message || isWaitingForResponse) return;
    
    // Add user message to chat
    addMessageToChat('user', message);
    
    // Clear input field
    userMessageInput.value = '';
    
    try {
        // Set waiting state
        isWaitingForResponse = true;
        
        // Add typing indicator
        addTypingIndicator();
        
        // Send message to API
        const response = await sendMessageToAPI(message);
        
        // Remove typing indicator
        removeTypingIndicator();
        
        // Add assistant response to chat
        addMessageToChat('assistant', response);
    } catch (error) {
        console.error('Error:', error);
        
        // Remove typing indicator
        removeTypingIndicator();
        
        // Add error message
        addMessageToChat('assistant', 'Sorry, I encountered an error. Please try again later.');
    } finally {
        isWaitingForResponse = false;
    }
});

/**
 * Send message to API and get response
 * @param {string} message - The user's message
 * @returns {Promise<string>} - The assistant's response
 */
async function sendMessageToAPI(message) {
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        return data.response || 'Sorry, I did not understand that.';
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

/**
 * Add a message to the chat
 * @param {string} role - Either 'user' or 'assistant'
 * @param {string} content - The message content
 */
function addMessageToChat(role, content) {
    // Create message element
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', role);
    
    // Create message content
    const contentDiv = document.createElement('div');
    contentDiv.classList.add('message-content');
    
    // Add text with proper formatting for links
    const paragraph = document.createElement('p');
    paragraph.innerHTML = formatMessage(content);
    
    // Append elements
    contentDiv.appendChild(paragraph);
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    scrollToBottom();
}

/**
 * Format message with links and basic formatting
 * @param {string} text - The raw text
 * @returns {string} - Formatted HTML
 */
function formatMessage(text) {
    // Convert URLs to clickable links
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    return text
        .replace(urlRegex, url => `<a href="${url}" target="_blank">${url}</a>`)
        .replace(/\n/g, '<br>');
}

/**
 * Add typing indicator to chat
 */
function addTypingIndicator() {
    const indicatorDiv = document.createElement('div');
    indicatorDiv.classList.add('message', 'assistant', 'typing-indicator');
    
    const contentDiv = document.createElement('div');
    contentDiv.classList.add('message-content');
    
    contentDiv.innerHTML = '<div class="typing-dots"><span></span><span></span><span></span></div>';
    
    indicatorDiv.appendChild(contentDiv);
    chatMessages.appendChild(indicatorDiv);
    
    scrollToBottom();
}

/**
 * Remove typing indicator from chat
 */
function removeTypingIndicator() {
    const typingIndicator = document.querySelector('.typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

/**
 * Scroll chat to bottom
 */
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Add typing indicator dots animation to CSS
const style = document.createElement('style');
style.textContent = `
.typing-dots {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
    height: 20px;
}

.typing-dots span {
    width: 8px;
    height: 8px;
    background-color: #aaa;
    border-radius: 50%;
    animation: typingDot 1.4s infinite ease-in-out;
}

.typing-dots span:nth-child(1) {
    animation-delay: 0s;
}

.typing-dots span:nth-child(2) {
    animation-delay: 0.2s;
}

.typing-dots span:nth-child(3) {
    animation-delay: 0.4s;
}

@keyframes typingDot {
    0%, 60%, 100% {
        transform: translateY(0);
    }
    30% {
        transform: translateY(-8px);
    }
}
`;
document.head.appendChild(style); 