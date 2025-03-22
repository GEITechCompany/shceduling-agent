/**
 * Scheduling Assistant Configuration
 * 
 * This file contains configuration settings for the Scheduling Assistant frontend.
 * Modify these settings to connect to your API backend.
 */

// Default configuration
const DEFAULT_CONFIG = {
    // API endpoint URL - will be updated based on environment
    apiUrl: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://localhost:5001/api/chat'
        : 'https://scheduling-gpt-assistant.herokuapp.com/api/chat',
    
    // API key (if required)
    apiKey: '',
    
    // App settings
    appName: 'Scheduling Assistant',
    
    // Company information
    company: {
        name: 'Window Cleaning Services',
        phone: '(555) 123-4567',
        email: 'contact@windowcleaning.com'
    },
    
    // Service information
    services: [
        {
            name: 'Window Cleaning',
            icon: 'fa-window-maximize',
            price: '$150-300 depending on size'
        },
        {
            name: 'Gutter Cleaning',
            icon: 'fa-water',
            price: '$100-200'
        },
        {
            name: 'Pressure Washing',
            icon: 'fa-spray-can',
            price: '$200-400'
        },
        {
            name: 'Solar Panel Cleaning',
            icon: 'fa-solar-panel',
            price: '$250-500'
        }
    ],
    
    // Business hours
    businessHours: 'Monday-Friday: 9 AM - 5 PM'
};

// Load stored configuration from localStorage if available
function loadConfig() {
    const storedConfig = localStorage.getItem('schedulingAssistantConfig');
    
    // If stored config exists, parse it and merge with default config
    if (storedConfig) {
        try {
            const parsedConfig = JSON.parse(storedConfig);
            return { ...DEFAULT_CONFIG, ...parsedConfig };
        } catch (error) {
            console.error('Error parsing stored config:', error);
            return DEFAULT_CONFIG;
        }
    }
    
    return DEFAULT_CONFIG;
}

// Save configuration to localStorage
function saveConfig(config) {
    localStorage.setItem('schedulingAssistantConfig', JSON.stringify(config));
}

// Current configuration (combination of default and stored)
const CONFIG = loadConfig();

// Export the configuration
window.SCHEDULING_ASSISTANT_CONFIG = CONFIG;

// Check if we should use a different API URL based on environment
// For example, when deployed on Hostinger
if (window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
    // If the API URL is still set to localhost, show a warning in the console
    if (CONFIG.apiUrl.includes('localhost')) {
        console.warn('Warning: Your application is deployed on a remote server but API URL is still set to localhost.');
        console.warn('Use the settings button to update your API URL to point to your deployed backend.');
    }
} 