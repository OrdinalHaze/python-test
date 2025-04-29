import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key securely
api_key = os.getenv("MY_API_KEY")

# Configure the API key
genai.configure(api_key=api_key)

# Select the model
model = genai.GenerativeModel("gemini-1.5-flash")

# Generate a response
response = model.generate_content("Whats an apple")

# Print the response
print(response.text)
