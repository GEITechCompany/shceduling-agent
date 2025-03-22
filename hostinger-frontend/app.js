/**
 * Scheduling Assistant App
 * Frontend JavaScript for the Scheduling Assistant application.
 */

// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const messageForm = document.getElementById('messageForm');
const userMessageInput = document.getElementById('userMessage');
const settingsButton = document.getElementById('settingsButton');
const settingsPanel = document.getElementById('settingsPanel');
const apiUrlInput = document.getElementById('apiUrl');
const apiKeyInput = document.getElementById('apiKey');
const saveSettingsButton = document.getElementById('saveSettings');
const closeSettingsButton = document.getElementById('closeSettings');

// Initial loading state
let isWaitingForResponse = false;

// Initialize the application
function initApp() {
    // Load settings into form
    apiUrlInput.value = CONFIG.apiUrl || '';
    apiKeyInput.value = CONFIG.apiKey || '';
    
    // Set up event listeners
    setupEventListeners();
    
    // Update page content from config
    updatePageFromConfig();
}

// Update page content from configuration
function updatePageFromConfig() {
    // Update document title
    document.title = `${CONFIG.appName} | ${CONFIG.company.name}`;
    
    // Update contact information
    const contactElements = document.querySelectorAll('.contact-info p');
    if (contactElements.length >= 2) {
        contactElements[0].textContent = `Phone: ${CONFIG.company.phone}`;
        contactElements[1].textContent = `Email: ${CONFIG.company.email}`;
    }
    
    // Update business hours
    const businessHoursElement = document.querySelector('.business-hours p');
    if (businessHoursElement) {
        businessHoursElement.textContent = CONFIG.businessHours;
    }
}

// Set up event listeners
function setupEventListeners() {
    // Message form submission
    messageForm.addEventListener('submit', handleMessageSubmit);
    
    // Settings panel
    settingsButton.addEventListener('click', () => {
        settingsPanel.classList.add('visible');
    });
    
    closeSettingsButton.addEventListener('click', () => {
        settingsPanel.classList.remove('visible');
    });
    
    saveSettingsButton.addEventListener('click', saveSettings);
}

// Handle message form submission
async function handleMessageSubmit(e) {
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
        addMessageToChat('assistant', `Sorry, I encountered an error. Please try again later. 
        
        Error details: ${error.message}`);
    } finally {
        isWaitingForResponse = false;
    }
}

/**
 * Send message to API and get response
 * @param {string} message - The user's message
 * @returns {Promise<string>} - The assistant's response
 */
async function sendMessageToAPI(message) {
    try {
        const headers = {
            'Content-Type': 'application/json'
        };
        
        // Add API key if configured
        if (CONFIG.apiKey) {
            headers['Authorization'] = `Bearer ${CONFIG.apiKey}`;
        }
        
        const response = await fetch(CONFIG.apiUrl, {
            method: 'POST',
            headers,
            body: JSON.stringify({ message })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Check if response has the expected format
        if (!data.hasOwnProperty('response')) {
            console.warn('Unexpected API response format:', data);
            return data.message || data.error || 'Received response in unexpected format.';
        }
        
        return data.response;
    } catch (error) {
        console.error('API Error:', error);
        
        // Specific error for connection issues
        if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
            throw new Error('Could not connect to the API. Please check your API URL in settings and ensure your backend is running.');
        }
        
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
    
    // Convert line breaks to <br> tags
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

/**
 * Save settings from the settings panel
 */
function saveSettings() {
    const newApiUrl = apiUrlInput.value.trim();
    const newApiKey = apiKeyInput.value.trim();
    
    // Validate API URL
    if (!newApiUrl) {
        alert('API URL cannot be empty.');
        return;
    }
    
    // Update configuration
    CONFIG.apiUrl = newApiUrl;
    CONFIG.apiKey = newApiKey;
    
    // Save to local storage
    saveConfig({
        apiUrl: newApiUrl,
        apiKey: newApiKey
    });
    
    // Close settings panel
    settingsPanel.classList.remove('visible');
    
    // Show confirmation message
    addMessageToChat('assistant', 'Settings saved! The application is now connected to ' + newApiUrl);
}

// Initialize the app when document is ready
document.addEventListener('DOMContentLoaded', initApp); 