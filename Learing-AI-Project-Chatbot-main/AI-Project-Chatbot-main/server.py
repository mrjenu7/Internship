from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import re
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load eco-friendly product database
eco_products = {
    'cleaning': [
        "For eco-friendly cleaning, try brands like Seventh Generation, Method, or Ecover. They use plant-based ingredients and come in recycled packaging.",
        "Consider using DIY cleaning solutions with vinegar, baking soda, and essential oils to reduce plastic waste and avoid harsh chemicals.",
        "Reusable microfiber cloths are a great sustainable alternative to disposable wipes for cleaning."
    ],
    'kitchen': [
        "For sustainable kitchen products, look for bamboo utensils, beeswax wraps instead of plastic wrap, and silicone food storage bags.",
        "Replace paper towels with washable, reusable cotton towels to reduce waste in your kitchen.",
        "Consider a compost bin for food scraps to reduce kitchen waste going to landfills."
    ],
    'bathroom': [
        "Eco-friendly bathroom options include bamboo toothbrushes, solid shampoo bars, and toilet paper made from recycled materials.",
        "Try plastic-free dental floss made from silk or bamboo charcoal, which comes in refillable glass containers.",
        "Reusable safety razors are a sustainable alternative to plastic disposable razors."
    ],
    'clothing': [
        "Look for clothing brands that use organic cotton, recycled materials, or Tencel (made from sustainably harvested wood pulp).",
        "Consider brands like Patagonia, Reformation, or Everlane that prioritize sustainable practices in their manufacturing.",
        "Thrifting and secondhand shopping is one of the most eco-friendly ways to buy clothes."
    ],
    'energy': [
        "Solar-powered chargers and power banks are great eco-friendly alternatives for your electronic devices.",
        "LED bulbs use up to 80% less energy than traditional incandescent bulbs and last much longer.",
        "Smart power strips can help reduce phantom energy usage from devices that stay plugged in."
    ],
    'water': [
        "Consider using a water filter instead of buying bottled water to reduce plastic waste.",
        "Low-flow showerheads and faucet aerators can significantly reduce your water consumption.",
        "Reusable water bottles made from stainless steel or glass are durable, eco-friendly alternatives to plastic bottles."
    ]
}

specific_products = {
    'bottle': "For eco-friendly water bottles, stainless steel options from brands like Klean Kanteen or Hydro Flask are durable and free from harmful chemicals. Glass bottles with silicone sleeves from brands like Lifefactory are another great option.",
    'bag': "Reusable shopping bags made from organic cotton, jute, or recycled materials are great eco-friendly alternatives to plastic bags. Brands like Baggu and ChicoBag offer durable, packable options in fun designs.",
    'straw': "Eco-friendly alternatives to plastic straws include stainless steel, bamboo, glass, or silicone straws. Many come with carrying cases and cleaning brushes for on-the-go use.",
    'coffee': "For sustainable coffee or tea, look for reusable coffee filters, compostable tea bags, or loose leaf tea infusers. A reusable coffee cup or travel mug can also significantly reduce waste from disposable cups.",
    'tea': "For sustainable coffee or tea, look for reusable coffee filters, compostable tea bags, or loose leaf tea infusers. A reusable coffee cup or travel mug can also significantly reduce waste from disposable cups."
}

@app.route('/api/chat', methods=['POST'])
def chat():
    # Get user message from request
    data = request.get_json()
    message = data.get('message', '').lower()
    
    # Generate response based on message content
    response = generate_response(message)
    
    # Return response as JSON
    return jsonify({"response": response})

@app.route('/api/genai', methods=['POST'])
def genai():
    """Handle requests to the Google GenAI API"""
    data = request.get_json()
    prompt = data.get('prompt', '')
    api_key = data.get('apiKey', '')
    model = data.get('model', 'gemini-2.0-flash')
    
    if not prompt or not api_key:
        return jsonify({"error": "Missing required parameters"}), 400
    
    try:
        # Call the Google GenAI API
        response = call_google_genai(prompt, api_key, model)
        return jsonify(response)
    except Exception as e:
        print(f"Error calling GenAI: {e}")
        return jsonify({"error": str(e)}), 500

def call_google_genai(prompt, api_key, model):
    """Call the Google GenAI API with the provided prompt"""
    url = "https://generativelanguage.googleapis.com/v1/models/{model}:generateContent".format(model=model)
    headers = {
        "Content-Type": "application/json"
    }
    
    # Add API key as query parameter
    url += f"?key={api_key}"
    
    payload = {
        "contents": [{
            "role": "user",
            "parts": [{"text": prompt}]
        }]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"API request failed with status code: {response.status_code}, response: {response.text}")
    
    response_json = response.json()
    
    # Parse the response to extract the generated text
    try:
        generated_text = response_json["candidates"][0]["content"]["parts"][0]["text"]
        return {"text": generated_text}
    except (KeyError, IndexError) as e:
        print(f"Error parsing GenAI response: {e}, response: {response_json}")
        raise Exception("Failed to parse GenAI response")

def generate_response(message):
    import random
    
    # Check for greetings
    if re.search(r'\b(hello|hi|hey)\b', message):
        return "Hello! I'm here to help you find eco-friendly product alternatives. What kind of products are you interested in?"
    
    # Check for thank you
    if re.search(r'\b(thank|thanks)\b', message):
        return "You're welcome! I'm happy to help you find sustainable alternatives. Is there anything else you'd like to know about eco-friendly products?"
    
    # Check for goodbye
    if re.search(r'\b(bye|goodbye)\b', message):
        return "Goodbye! Remember, every small sustainable choice makes a difference. Feel free to come back whenever you need eco-friendly product recommendations!"
    
    # Check for product categories
    for category in eco_products:
        if category in message:
            return random.choice(eco_products[category])
    
    # Check for specific product types
    for product in specific_products:
        if product in message:
            return specific_products[product]
    
    # Fallback response if no keywords match
    return "I don't have specific information about that, but generally, look for products that are reusable, made from sustainable materials (like bamboo, organic cotton, or recycled materials), and come in minimal or plastic-free packaging. Can you be more specific about what type of eco-friendly product you're looking for?"

if __name__ == '__main__':
    app.run(debug=True, port=5000) 
