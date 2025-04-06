import google.generativeai as genai

# Configure the API key
genai.configure(api_key="AIzaSyB6ovP-Tabw7xgyZGfzcVT_bBcY05lcWLI")

# Select the model
model = genai.GenerativeModel("gemini-1.5-flash")  # Use the correct model name

# Generate a response
response = model.generate_content("Which is the first stage in every IoT architecture?")

# Print the response
print(response.text)
