from openai import OpenAI
import logging

# Replace with your OpenAI API key
API_KEY = "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"

# Configure logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger("OpenAITest")

def ask_to_ai(prompt, tier="bronze"):
    """
    Sends a prompt to the OpenAI API and enforces rigid responses through function calling.

    Args:
        prompt (str): The user's input or query.
        tier (str): The level of detail or assistance (bronze, silver, gold).

    Yields:
        str: The AI-generated response tokens.
    """
    try:
        client = OpenAI(api_key=API_KEY)

        # Define functions for rigid response enforcement
        functions = []

        if tier == "bronze":
            functions = [
                {
                    "name": "provide_debugging_tips",
                    "description": "Provide exactly three debugging tips without solving the user's problem.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "tips": {
                                "type": "array",
                                "items": {"type": "string"},
                                "maxItems": 3,
                                "minItems": 3
                            }
                        },
                        "required": ["tips"]
                    }
                }
            ]
        elif tier == "silver":
            functions = [
                {
                    "name": "explain_concept",
                    "description": "Explain the concept relevant to the query without solving the problem or giving direct code.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "concept": {"type": "string"}
                        },
                        "required": ["concept"]
                    }
                }
            ]
        elif tier == "gold":
            functions = [
                {
                    "name": "provide_targeted_solution",
                    "description": "Provide a direct and specific solution to the problem described.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "solution": {"type": "string"}
                        },
                        "required": ["solution"]
                    }
                }
            ]
        else:
            raise ValueError("Invalid tier specified")

        logger.info(f"Sending prompt to OpenAI API with tier '{tier}': {prompt}")

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant strictly following the instructions."},
                {"role": "user", "content": prompt}
            ],
            functions=functions,
            function_call={"name": functions[0]["name"]}  # Force specific function
        )

        # Log raw response for debugging
        logger.info(f"Raw API response: {response}")

        # Extract and handle function call output
        try:
            if response.choices:  # Check if there are choices
                choice = response.choices[0]  # Get the first choice
                if choice.message and choice.message.function_call:
                    function_call = choice.message.function_call
                    if function_call.arguments:
                        function_output = function_call.arguments
                        logger.info(f"Function output: {function_output}")
                        yield function_output
                    else:
                        raise ValueError("Function call exists but has no arguments.")
                else:
                    raise ValueError("Function call missing in the message.")
            else:
                raise ValueError("No valid choices in the response.")
        except ValueError as ve:
            logger.error(f"Error querying OpenAI API: {ve}")
            yield f"Error: {ve}"

    except Exception as e:
        logger.error(f"Unexpected error in ask_to_ai: {e}")
        yield f"Error: {e}"


