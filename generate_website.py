import os
import requests
import json

# WARNING: This script has the API key hard-coded for simplicity.
# This is NOT a a best practice for production code.
api_key = "AIzaSyCmPHf7XcMqOiMAIni7rnemnpLsmalDFug"

if not api_key:
    print("Error: The API key is missing from the script.")
    exit()

# Define the model and API endpoint
GEMINI_MODEL = "gemini-2.5-flash-preview-05-20"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

def generate_page(page_name, prompt):
    """
    Sends a prompt to the Gemini API to generate HTML, CSS, and JS for a single page.
    """
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "key": api_key
    }
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Generate a single-file HTML website with Tailwind CSS. This is the {page_name} page for a professional plumbing website. It must link to home, services, and contact pages using the filenames 'index.html', 'services.html', and 'contact.html'. The content should be about: {prompt}"
                    }
                ]
            }
        ]
    }

    print(f"Generating code for the {page_name} page with Gemini...")
    try:
        response = requests.post(API_URL, headers=headers, params=params, data=json.dumps(data))
        response.raise_for_status()
        
        result = response.json()
        generated_text = result['candidates'][0]['content']['parts'][0]['text']
        return generated_text

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except KeyError:
        print("Failed to parse the Gemini API response.")
        return None

if __name__ == "__main__":
    
    # Prompt for the Home page
    home_page_prompt = "A professional home page for a plumbing service. Include a hero section, a short 'About Us' section, and a list of key services."
    home_page_code = generate_page("Home", home_page_prompt)
    
    if home_page_code:
        with open("index.html", "w") as f:
            f.write(home_page_code)
        print("Home page (index.html) generated successfully!")

    # Prompt for the Services page
    services_page_prompt = "A detailed services page for a plumbing service. Include sections for emergency repairs, drain cleaning, water heater installation, and new installations."
    services_page_code = generate_page("Services", services_page_prompt)
    
    if services_page_code:
        with open("services.html", "w") as f:
            f.write(services_page_code)
        print("Services page (services.html) generated successfully!")
        
    # Prompt for the Contact page
    contact_page_prompt = "A contact page for a plumbing service with a contact form, phone number, email address, and a map of the service area."
    contact_page_code = generate_page("Contact", contact_page_prompt)
    
    if contact_page_code:
        with open("contact.html", "w") as f:
            f.write(contact_page_code)
        print("Contact page (contact.html) generated successfully!")
        
    print("\nWebsite generation complete. You now have a three-page plumbing website.")
