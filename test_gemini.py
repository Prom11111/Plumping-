import requests

# Your Gemini API key
API_KEY = "AIzaSyCmPHf7XcMqOiMAIni7rnemnpLsmalDFug"

# The Gemini API endpoint for text generation
URL = "https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText"

# Prompt for generating a simple website
prompt = """
Create a basic 1-page HTML website with:
- A header that says "Welcome to My Website"
- A paragraph with "This website is powered by Gemini API"
- A footer with "Contact: example@example.com"
"""

# Request payload
data = {
    "prompt": {
        "text": prompt
    },
    "temperature": 0.5,
    "maxOutputTokens": 300
}

# Headers
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Make the request
response = requests.post(URL, json=data, headers=headers)

if response.status_code == 200:
    result = response.json()
    text_output = result.get("candidates", [{}])[0].get("output", "")
    
    # Save to HTML file
    with open("generated_website.html", "w") as f:
        f.write(text_output)
    
    print("Website generated and saved as generated_website.html!")
else:
    print("Error:", response.status_code, response.text)
