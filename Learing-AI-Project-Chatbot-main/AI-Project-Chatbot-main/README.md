# Eco-Bot: Eco-Friendly Product Recommendation Chatbot

A web-based chatbot that provides real-time information about eco-friendly products using Google's Generative AI (Gemini). The chatbot uses HTML, CSS, and JavaScript with direct API integration to Gemini AI for intelligent, contextual responses about sustainable products.

## Features

- Modern, responsive UI with dark mode toggle
- Real-time chat interface with typing indicators
- **Direct integration with Google's Gemini AI**
- Real-time, AI-generated responses about eco-friendly products
- Chat history stored in localStorage
- Ability to download chat history as a text file
- Response rating system
- Student information panel

## Project Structure

```
eco-bot/
├── index.html            # Main HTML file
├── css/
│   └── style.css         # CSS styling
└── js/
    └── main.js           # Frontend JavaScript with direct Gemini AI integration
```

## Setup and Installation

### Prerequisites

- Web browser (Chrome, Firefox, etc.)
- Internet connection for API access

### Setup

1. Clone or download this repository
2. Open `index.html` in your web browser

## Usage

1. Open `index.html` in your web browser
2. Type your query about eco-friendly products in the input field
3. Press Enter or click the send button to get AI-generated recommendations
4. Use the dark mode toggle to switch between light and dark themes
5. Clear chat history or download your conversation using the buttons at the bottom

## API Integration

The chatbot directly integrates with Google's Gemini AI for real-time responses about eco-friendly products:

```javascript
// Direct call to Gemini API
fetch('https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key=API_KEY', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        contents: [{
            role: "user",
            parts: [{ text: "User prompt about eco-friendly products" }]
        }]
    })
})
.then(response => response.json())
.then(data => {
    // Process the AI response
});
```

## Customization

You can customize the chatbot by:

1. Modifying the CSS in `style.css` to change the look and feel
2. Adding student information in the HTML file
3. Adjusting the prompts sent to Google Gemini AI in the `callGeminiAI` function

## License

This project is open source and available for educational purposes.

## Contributors

- Student Name (Registration #, Roll #)
- Student Name (Registration #, Roll #) 