# python code

import requests

# URL for the API endpoint
url = 'https://5c85-34-16-0-60.ngrok-free.app/api/generate'

# Function to make the POST request
def make_request(prompt):
    data = {
        "model": "llama2",
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json().get("response", "No response received")
    else:
        return f"Error: {response.status_code}, {response.text}"

# Continuous chat loop
while True:
    # Get user input for the prompt
    prompt = input("You: ")

    # Check if the user wants to exit
    if prompt.lower() == 'exit':
        print("Exiting chat.")
        break

    # Make the request
    response = make_request(prompt)

    # Print the response
    print("Bot:", response)
