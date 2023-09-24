
from decouple import config
import bard

# Get the API key.
api_key = "YOUR_API_KEY"

# Create a Bard client.
client = bard.BardClient(api_key)

# Send a request to the API.
response = client.retrieve("What is the capital of France?")

# Print the response.
print(response)