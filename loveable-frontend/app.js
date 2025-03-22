// Remove ES module imports and use CDN scripts instead
const supabaseUrl = 'https://fhuxuwgvlgtmubxvsnil.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZodXh1d2d2bGd0bXVieHZzbmlsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTA5ODQwMDAsImV4cCI6MjAyNjU2MDAwMH0.UYY8YvHaFfvlFJWxHRBDyXRHj_Qa-dGXhsGVQYGQRQE';
const supabase = supabaseClient.createClient(supabaseUrl, supabaseKey);

// Import FullCalendar and its plugins
import { Calendar } from '@fullcalendar/core';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';

// DOM Elements
const appointmentForm = document.getElementById('appointmentForm');
const serviceSelect = document.getElementById('service');
const servicesList = document.getElementById('servicesList');
const loginBtn = document.getElementById('loginBtn');
const calendarEl = document.getElementById('calendar');

// Additional DOM Elements for Chat
const chatWidget = document.getElementById('chatWidget');
const chatContent = document.getElementById('chatContent');
const toggleChat = document.getElementById('toggleChat');
const chatMessages = document.getElementById('chatMessages');
const chatForm = document.getElementById('chatForm');
const messageInput = document.getElementById('messageInput');

// State
let currentUser = null;
let calendar = null;

// Scheduling agent responses
const agentResponses = {
    greetings: [
        "Hello! I'm your scheduling assistant. How can I help you today?",
        "Hi there! Need help with scheduling an appointment?",
        "Welcome! I can help you find the perfect time slot for your appointment."
    ],
    availability: [
        "I'll check the available time slots for you.",
        "Let me find some open appointments that work for you.",
        "I'll look up the schedule right away."
    ],
    confirmation: [
        "Great! I've found some available slots.",
        "Perfect! Here are the available times.",
        "I can help you book that time slot."
    ]
};

// Initialize the application
async function initializeApp() {
    await loadServices();
    setupEventListeners();
    checkAuth();
    initializeCalendar();
    initializeChat();
}

// Initialize FullCalendar
function initializeCalendar() {
    calendar = new Calendar(calendarEl, {
        plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
        initialView: 'timeGridWeek',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        events: fetchCalendarEvents,
        eventClick: handleEventClick,
        dateClick: handleDateClick,
        height: '600px'
    });

    calendar.render();
}

// Fetch calendar events from Supabase
async function fetchCalendarEvents(info, successCallback, failureCallback) {
    try {
        const { data, error } = await supabase
            .from('schedules')
            .select('*, clients(name), services(name)')
            .gte('service_date', info.start.toISOString())
            .lte('service_date', info.end.toISOString());

        if (error) throw error;

        const events = data.map(schedule => ({
            id: schedule.id,
            title: `${schedule.clients.name} - ${schedule.services.name}`,
            start: `${schedule.service_date}T${schedule.start_time}`,
            end: `${schedule.service_date}T${schedule.end_time}`,
            extendedProps: {
                clientName: schedule.clients.name,
                serviceName: schedule.services.name,
                status: schedule.status,
                notes: schedule.notes || ''
            }
        }));

        successCallback(events);
    } catch (error) {
        console.error('Error fetching events:', error);
        failureCallback(error);
    }
}

// Handle calendar event click
function handleEventClick(info) {
    const event = info.event;
    showEventDetails(event);
}

// Handle calendar date click
function handleDateClick(info) {
    document.getElementById('date').value = info.dateStr;
    document.getElementById('time').value = '09:00';
    appointmentForm.scrollIntoView({ behavior: 'smooth' });
}

// Show event details in a modal
function showEventDetails(event) {
    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
    modal.innerHTML = `
        <div class="bg-white p-6 rounded-lg max-w-lg w-full mx-4">
            <h3 class="text-xl font-semibold mb-4">${event.title}</h3>
            <p class="mb-2"><strong>Status:</strong> ${event.extendedProps.status}</p>
            <p class="mb-2"><strong>Time:</strong> ${event.start.toLocaleTimeString()} - ${event.end.toLocaleTimeString()}</p>
            <p class="mb-4"><strong>Notes:</strong> ${event.extendedProps.notes}</p>
            <div class="flex justify-end space-x-2">
                <button onclick="this.closest('.fixed').remove()" 
                        class="px-4 py-2 bg-gray-200 rounded-lg hover:bg-gray-300">
                    Close
                </button>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
}

// Load services from Supabase
async function loadServices() {
    try {
        const { data: services, error } = await supabase
            .from('services')
            .select('*');

        if (error) throw error;

        // Populate service select
        services.forEach(service => {
            const option = document.createElement('option');
            option.value = service.id;
            option.textContent = service.name;
            serviceSelect.appendChild(option);
        });

        // Populate services list
        servicesList.innerHTML = services.map(service => `
            <div class="service-card">
                <h3 class="text-lg font-semibold mb-2">${service.name}</h3>
                <p class="text-gray-600 mb-4">${service.description}</p>
                <div class="flex justify-between items-center">
                    <span class="text-purple-600 font-semibold">$${service.price}</span>
                    <button onclick="bookService(${service.id})" 
                            class="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700">
                        Book Now
                    </button>
                </div>
            </div>
        `).join('');

    } catch (error) {
        showToast('Error loading services', 'error');
        console.error('Error:', error);
    }
}

// Handle appointment booking
async function handleAppointmentSubmit(event) {
    event.preventDefault();
    
    if (!currentUser) {
        showToast('Please log in to book an appointment', 'warning');
        return;
    }

    const formData = {
        service_id: serviceSelect.value,
        date: document.getElementById('date').value,
        time: document.getElementById('time').value,
        notes: document.getElementById('notes').value,
        client_id: currentUser.id,
        status: 'pending'
    };

    try {
        const { data, error } = await supabase
            .from('schedules')
            .insert([formData]);

        if (error) throw error;

        showToast('Appointment booked successfully!', 'success');
        appointmentForm.reset();
        calendar.refetchEvents();
        
    } catch (error) {
        showToast('Error booking appointment', 'error');
        console.error('Error:', error);
    }
}

// Handle login
async function handleLogin() {
    if (currentUser) {
        // Logout if already logged in
        await supabase.auth.signOut();
        currentUser = null;
        loginBtn.textContent = 'Login';
        showToast('Logged out successfully', 'success');
        return;
    }

    // For demo purposes, we'll use magic link login
    const email = prompt('Please enter your email:');
    if (!email) return;

    try {
        const { error } = await supabase.auth.signInWithOtp({
            email: email
        });

        if (error) throw error;

        showToast('Check your email for login link', 'success');
    } catch (error) {
        showToast('Error sending login link', 'error');
        console.error('Error:', error);
    }
}

// Check authentication status
async function checkAuth() {
    const { data: { user } } = await supabase.auth.getUser();
    if (user) {
        currentUser = user;
        loginBtn.textContent = 'Logout';
    }
}

// Setup event listeners
function setupEventListeners() {
    appointmentForm.addEventListener('submit', handleAppointmentSubmit);
    loginBtn.addEventListener('click', handleLogin);

    // Chat event listeners
    toggleChat.addEventListener('click', () => {
        chatContent.classList.remove('hidden');
        messageInput.focus();
        
        if (chatMessages.children.length === 0) {
            const greeting = agentResponses.greetings[Math.floor(Math.random() * agentResponses.greetings.length)];
            addSystemMessage(greeting);
        }
    });

    // Update chat form submission
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = messageInput.value.trim();
        if (message) {
            messageInput.value = '';
            await sendMessage(message);
        }
    });
}

// Utility function to show toast notifications
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);

    // Show toast
    setTimeout(() => toast.classList.add('show'), 100);

    // Hide and remove toast
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Book service directly from service card
function bookService(serviceId) {
    serviceSelect.value = serviceId;
    appointmentForm.scrollIntoView({ behavior: 'smooth' });
}

// Initialize Chat
async function initializeChat() {
    try {
        if (!chatMessages || !chatForm || !messageInput) {
            console.error('Chat elements not found');
            return;
        }

        chatMessages.innerHTML = '';
        
        const greeting = "Hello! I'm your scheduling assistant. How can I help you today?";
        addSystemMessage(greeting);

        // Setup chat form submission
        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const message = messageInput.value.trim();
            if (message) {
                messageInput.value = '';
                await sendMessage(message);
            }
        });

    } catch (error) {
        console.error('Error initializing chat:', error);
        addSystemMessage("There was an error initializing the chat. Please refresh the page.");
    }
}

// Update sendMessage function
async function sendMessage(content) {
    try {
        // Add user message to chat immediately
        const userMessageElement = document.createElement('div');
        userMessageElement.className = 'message sent';
        userMessageElement.innerHTML = `
            <div class="message-content">${content}</div>
            <div class="message-time">${new Date().toLocaleTimeString()}</div>
        `;
        chatMessages.appendChild(userMessageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // Show typing indicator
        const typingIndicator = document.createElement('div');
        typingIndicator.className = 'agent-typing';
        typingIndicator.innerHTML = `
            <span>Agent is typing</span>
            <div class="typing-indicator">
                <span></span><span></span><span></span>
            </div>
        `;
        chatMessages.appendChild(typingIndicator);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // Send message to server
        const response = await fetch('http://localhost:5001/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: content })
        });

        if (!response.ok) {
            throw new Error('Failed to get response from server');
        }

        const data = await response.json();

        // Remove typing indicator
        typingIndicator.remove();

        // Add agent response to chat
        addSystemMessage(data.response);

    } catch (error) {
        console.error('Error in chat:', error);
        addSystemMessage("I'm sorry, I'm having trouble processing your request. Please try again.");
    }
}

// Add a system message
function addSystemMessage(content) {
    const messageElement = document.createElement('div');
    messageElement.className = 'message received';
    messageElement.innerHTML = `
        <div class="message-content">${content}</div>
        <div class="message-time">${new Date().toLocaleTimeString()}</div>
    `;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeApp); 