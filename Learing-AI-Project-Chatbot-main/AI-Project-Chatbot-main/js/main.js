document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const chatMessages = document.getElementById('chatMessages');
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');
    const clearBtn = document.getElementById('clearBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const themeToggle = document.querySelector('.theme-toggle');
    const aiStatus = document.getElementById('aiStatus');
    
    // Initialize Google GenAI
    const API_KEY = "AIzaSyBUQ2cqd3Thv4xfkazNvuzYrf2FNiKxb3w";
    
    // Chat history from localStorage
    let chatHistory = JSON.parse(localStorage.getItem('ecoBotChatHistory')) || [];
    
    // Load chat history if available
    if (chatHistory.length > 0) {
        chatHistory.forEach(message => {
            addMessageToUI(message.text, message.sender);
        });
    }
    
    // Event Listeners
    sendBtn.addEventListener('click', handleUserMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleUserMessage();
        }
    });
    
    clearBtn.addEventListener('click', clearChat);
    downloadBtn.addEventListener('click', downloadChat);
    themeToggle.addEventListener('click', toggleTheme);
    
    // Check for saved theme preference
    if (localStorage.getItem('darkMode') === 'enabled') {
        document.body.classList.add('dark-mode');
        themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    }
    
    // Functions
    function handleUserMessage() {
        const message = userInput.value.trim();
        if (message === '') return;
        
        // Add user message to UI
        addMessageToUI(message, 'user');
        
        // Save to history
        saveToHistory(message, 'user');
        
        // Clear input
        userInput.value = '';
        
        // Process the message and get a response
        processUserMessage(message);
    }
    
    async function processUserMessage(message) {
        // Show typing indicator
        showTypingIndicator();
        
        try {
            // Call the Gemini AI API directly
            const response = await callGeminiAI(message);
            if (response) {
                // Update AI status indicator
                updateAIStatus('Gemini');
                
                // Remove typing indicator
                removeTypingIndicator();
                
                // Add bot response to UI
                addMessageToUI(response, 'bot');
                
                // Save to history
                saveToHistory(response, 'bot');
                
                // Add rating buttons to the last bot message
                addRatingToLastMessage();
                return;
            } else {
                throw new Error("Failed to get response from Gemini AI");
            }
        } catch (error) {
            console.error('Error:', error);
            
            // Update AI status indicator to show error
            updateAIStatus('Error');
            
            // Remove typing indicator
            removeTypingIndicator();
            
            // Add error message to UI
            addMessageToUI("I'm having trouble connecting to my knowledge base right now. Please try again in a moment.", 'bot');
            
            // Save to history
            saveToHistory("I'm having trouble connecting to my knowledge base right now. Please try again in a moment.", 'bot');
            
            // Add rating buttons
            addRatingToLastMessage();
        }
    }
    
    async function callGeminiAI(message) {
        try {
            // Format the prompt to focus on eco-friendly products
            const prompt = `The user is asking about eco-friendly products: "${message}". 
            Provide helpful, accurate information about sustainable and eco-friendly products related to their query.
            Focus on environmentally friendly alternatives, sustainable materials, or eco-conscious practices.
            If the query is not clear, ask for clarification about what specific eco-friendly products they're interested in.
            Keep the response concise but informative.`;
            
            // Call the Gemini API directly
            const response = await fetch('https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key=' + API_KEY, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    contents: [{
                        role: "user",
                        parts: [{ text: prompt }]
                    }]
                })
            });
            
            if (!response.ok) {
                throw new Error(`API request failed with status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Extract the generated text from the response
            try {
                return data.candidates[0].content.parts[0].text;
            } catch (e) {
                console.error('Error parsing API response:', e, data);
                return null;
            }
        } catch (error) {
            console.error('Error calling Gemini AI:', error);
            return null;
        }
    }
    
    function updateAIStatus(status) {
        aiStatus.textContent = status;
        
        // Change the color based on the AI being used
        const aiBadge = aiStatus.parentElement;
        const statusColors = {
            'Gemini': '#4cff4c', // Green
            'Error': '#ff5252' // Red
        };
        
        aiBadge.style.setProperty('--indicator-color', statusColors[status] || '#4cff4c');
        
        // Add animation for status change
        aiBadge.classList.add('status-change');
        setTimeout(() => {
            aiBadge.classList.remove('status-change');
        }, 600);
    }
    
    function addMessageToUI(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${sender}-message`);
        
        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');
        
        const paragraph = document.createElement('p');
        paragraph.textContent = text;
        
        contentDiv.appendChild(paragraph);
        messageDiv.appendChild(contentDiv);
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.classList.add('message', 'bot-message', 'typing-indicator');
        
        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');
        
        contentDiv.innerHTML = '<span></span><span></span><span></span>';
        typingDiv.appendChild(contentDiv);
        chatMessages.appendChild(typingDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    function removeTypingIndicator() {
        const typingIndicator = document.querySelector('.typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    function saveToHistory(text, sender) {
        chatHistory.push({ text, sender });
        localStorage.setItem('ecoBotChatHistory', JSON.stringify(chatHistory));
    }
    
    function clearChat() {
        chatMessages.innerHTML = '';
        chatHistory = [];
        localStorage.removeItem('ecoBotChatHistory');
        
        // Add the welcome message back
        const welcomeMessage = "Hello! I'm Eco-Bot. Ask me about eco-friendly products and sustainable alternatives.";
        addMessageToUI(welcomeMessage, 'bot');
        saveToHistory(welcomeMessage, 'bot');
        
        // Reset AI status
        updateAIStatus('Gemini');
    }
    
    function downloadChat() {
        if (chatHistory.length <= 1) {
            alert("There's not enough chat history to download.");
            return;
        }
        
        let chatText = "Eco-Bot Chat History\n\n";
        chatHistory.forEach(message => {
            const sender = message.sender === 'user' ? 'You' : 'Eco-Bot';
            chatText += `${sender}: ${message.text}\n\n`;
        });
        
        const blob = new Blob([chatText], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'eco-bot-chat.txt';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
    
    function toggleTheme() {
        if (document.body.classList.contains('dark-mode')) {
            document.body.classList.remove('dark-mode');
            themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
            localStorage.setItem('darkMode', 'disabled');
        } else {
            document.body.classList.add('dark-mode');
            themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
            localStorage.setItem('darkMode', 'enabled');
        }
    }
    
    function addRatingToLastMessage() {
        const lastBotMessage = chatMessages.querySelector('.bot-message:last-child .message-content');
        if (!lastBotMessage) return;
        
        const ratingDiv = document.createElement('div');
        ratingDiv.classList.add('rating');
        ratingDiv.innerHTML = `
            <span>Was this helpful?</span>
            <button class="rating-btn" data-rating="thumbsup"><i class="fas fa-thumbs-up"></i></button>
            <button class="rating-btn" data-rating="thumbsdown"><i class="fas fa-thumbs-down"></i></button>
        `;
        
        lastBotMessage.appendChild(ratingDiv);
        
        // Add event listeners for rating buttons
        const ratingButtons = ratingDiv.querySelectorAll('.rating-btn');
        ratingButtons.forEach(button => {
            button.addEventListener('click', () => {
                ratingButtons.forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');
                
                // In a real app, you might want to send this rating to your backend
                const rating = button.getAttribute('data-rating');
                console.log('User rated:', rating);
            });
        });
    }
}); 