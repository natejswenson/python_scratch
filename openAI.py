"""OpenAI API integration example."""
from decouple import config
from openai import OpenAI

def main():
    """Main function to demonstrate OpenAI API usage."""
    # Get the API key from environment
    api_key = config('open_ai_pat')

    # Create OpenAI client
    client = OpenAI(api_key=api_key)

    # Send a request to the API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "What is the capital of France?"}
        ]
    )

    # Print the response
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()