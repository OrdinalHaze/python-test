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

while True:
    x = input("Enter your prompt: ")
    
    if x.lower() == "exit":
        print("Exiting the program.")
        break
    
    # Generate a response
    response = model.generate_content(x)
    print(response.text)
    print("If you want to stop, type 'exit'")
