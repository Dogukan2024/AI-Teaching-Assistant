from openai import OpenAI
import logging

# Replace with your OpenAI API key
API_KEY = "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"

# Configure logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger("OpenAITest")

# Function to interact with OpenAI API
from openai import OpenAI

client = OpenAI(api_key=API_KEY)

def ask_to_ai(prompt, tier="bronze", history=None):
    """
    Sends a prompt to the OpenAI API using gpt-4o and maintains threaded chat with tier-specific instructions.
    Streams response chunks in real-time.

    Args:
        prompt (str): The user's input or query.
        tier (str): The level of detail or assistance (bronze, silver, gold).
        history (list): The message history to maintain threaded chat.

    Yields:
        str: The AI-generated response tokens streamed in real-time.
    """
    try:
        # Initialize history if this is the first interaction
        if history is None:
            history = []

        # Define tier-specific system instructions
        if tier == "bronze":
            instructions = (
                "You are a helpful assistant focused on debugging tips and basic clarifications. "
                "Guide the user to understand their issue without solving it for them."
            )
        elif tier == "silver":
            instructions = (
                "You are a helpful assistant providing indirect guidance. "
                "Offer conceptual explanations and ideas to guide the user without giving a complete solution."
            )
        elif tier == "gold":
            instructions = (
                "You are a helpful assistant providing targeted solutions. "
                "If the user provides code, suggest specific fixes and improvements."
            )
        else:
            instructions = "You are a helpful assistant."

        # Ensure the first system message reflects the current tier
        history = [msg for msg in history if msg["role"] != "system"]
        history.insert(0, {"role": "system", "content": instructions})

        # Add the user's query to the conversation history
        history.append({"role": "user", "content": prompt})

        # Send the request to the OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=history,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True  # Enable streaming
        )

        # Stream the response content in real-time
        response_content = ""
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                content_chunk = chunk.choices[0].delta.content
                response_content += content_chunk
                yield content_chunk  # Stream each chunk to the user in real-time

        # Add the assistant's response to the history
        history.append({"role": "assistant", "content": response_content})

    except Exception as e:
        yield f"Error: {str(e)}"

    return history  # Return the updated history
