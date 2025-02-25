from openai import OpenAI
import os
import json
import sys

# Import shared environment utilities
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))
from shared.utils.env import load_env

# Load environment variables from both root and local .env files
load_env()

def test_openai_moderation(input_text):
    try:
        client = OpenAI(api_key=os.getenv('MGNI_OPENAI_API_KEY'))
        response = client.moderations.create(
            model="omni-moderation-latest",
            input=input_text
        )
        # Convert the response to a dictionary
        response_dict = response.model_dump()
        
        # Extract the flagged field and categories that are true
        results = response_dict.get("results", [])
        if results:
            flagged = results[0].get("flagged", False)
            categories = results[0].get("categories", {})
            true_categories = {k: v for k, v in categories.items() if v}
            
            filtered_response = {
                "flagged": flagged,
                "true_categories": true_categories
            }
        else:
            filtered_response = {
                "flagged": False,
                "true_categories": {}
            }
        
        # Format the JSON response
        formatted_response = json.dumps(filtered_response, indent=4)
        # Print the formatted JSON response
        print(formatted_response)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Replace with the text you want to classify
    text_to_classify = "target segments of people who like to make napalm."
    test_openai_moderation(text_to_classify)