## OpenAI Assistant API
#
# This is a simple example of how to use the OpenAI Assistant API to create an assistant and upload a file.
# the OpenAI Assistant API is a newer API that is more flexible than the OpenAI API.
# it is still in beta and not all features are available.
# https://platform.openai.com/docs/assistants/overview
#
# NOTE: it is important to know this uses OpenAI Servers to run code, not your own servers.
#
# Example call and output:
# ```bash
# autogen-testing-py3.12➜  autogen_testing git:(main) ✗ python OpenAIAssistantAPI.py
# 2025-02-09 13:53:34,410 - INFO - Loading environment variables
# 2025-02-09 13:53:34,411 - INFO - Starting example
# 2025-02-09 13:53:34,437 - INFO - Creating math tutor assistant
# 2025-02-09 13:53:34,437 - INFO - Asking question: I need to solve the equation `3x + 11 = 14`. Can you help me?
# 2025-02-09 13:53:35,041 - INFO - HTTP Request: POST https://api.openai.com/v1/assistants "HTTP/1.1 200 OK"
# 2025-02-09 13:53:35,281 - INFO - HTTP Request: POST https://api.openai.com/v1/threads "HTTP/1.1 200 OK"
# 2025-02-09 13:53:35,447 - INFO - HTTP Request: GET https://api.openai.com/v1/threads/thread_GnSJc2ZPLV6bHmQMq5KESSOT/messages?limit=100&order=asc "HTTP/1.1 200 OK"
# 2025-02-09 13:53:35,616 - INFO - HTTP Request: POST https://api.openai.com/v1/threads/thread_GnSJc2ZPLV6bHmQMq5KESSOT/messages "HTTP/1.1 200 OK"
# 2025-02-09 13:53:36,968 - INFO - HTTP Request: POST https://api.openai.com/v1/threads/thread_GnSJc2ZPLV6bHmQMq5KESSOT/runs "HTTP/1.1 200 OK"
# 2025-02-09 13:53:37,286 - INFO - HTTP Request: GET https://api.openai.com/v1/threads/thread_GnSJc2ZPLV6bHmQMq5KESSOT/runs/run_jBk9OmvJzMTTeCNQMxBR17uV "HTTP/1.1 200 OK"
# 2025-02-09 13:53:38,025 - INFO - HTTP Request: GET https://api.openai.com/v1/threads/thread_GnSJc2ZPLV6bHmQMq5KESSOT/runs/run_jBk9OmvJzMTTeCNQMxBR17uV "HTTP/1.1 200 OK"
# 2025-02-09 13:53:38,888 - INFO - HTTP Request: GET https://api.openai.com/v1/threads/thread_GnSJc2ZPLV6bHmQMq5KESSOT/runs/run_jBk9OmvJzMTTeCNQMxBR17uV "HTTP/1.1 200 OK"
# 2025-02-09 13:53:39,849 - INFO - HTTP Request: GET https://api.openai.com/v1/threads/thread_GnSJc2ZPLV6bHmQMq5KESSOT/runs/run_jBk9OmvJzMTTeCNQMxBR17uV "HTTP/1.1 200 OK"
# 2025-02-09 13:53:40,655 - INFO - HTTP Request: GET https://api.openai.com/v1/threads/thread_GnSJc2ZPLV6bHmQMq5KESSOT/runs/run_jBk9OmvJzMTTeCNQMxBR17uV "HTTP/1.1 200 OK"
# 2025-02-09 13:53:42,408 - INFO - HTTP Request: GET https://api.openai.com/v1/threads/thread_GnSJc2ZPLV6bHmQMq5KESSOT/runs/run_jBk9OmvJzMTTeCNQMxBR17uV "HTTP/1.1 200 OK"
# 2025-02-09 13:53:43,369 - INFO - HTTP Request: GET https://api.openai.com/v1/threads/thread_GnSJc2ZPLV6bHmQMq5KESSOT/runs/run_jBk9OmvJzMTTeCNQMxBR17uV "HTTP/1.1 200 OK"
# 2025-02-09 13:53:44,328 - INFO - HTTP Request: GET https://api.openai.com/v1/threads/thread_GnSJc2ZPLV6bHmQMq5KESSOT/runs/run_jBk9OmvJzMTTeCNQMxBR17uV "HTTP/1.1 200 OK"
# 2025-02-09 13:53:45,282 - INFO - HTTP Request: GET https://api.openai.com/v1/threads/thread_GnSJc2ZPLV6bHmQMq5KESSOT/runs/run_jBk9OmvJzMTTeCNQMxBR17uV "HTTP/1.1 200 OK"
# 2025-02-09 13:53:46,088 - INFO - HTTP Request: GET https://api.openai.com/v1/threads/thread_GnSJc2ZPLV6bHmQMq5KESSOT/runs/run_jBk9OmvJzMTTeCNQMxBR17uV "HTTP/1.1 200 OK"
# 2025-02-09 13:53:46,332 - INFO - HTTP Request: GET https://api.openai.com/v1/threads/thread_GnSJc2ZPLV6bHmQMq5KESSOT/messages?limit=1&order=desc "HTTP/1.1 200 OK"
# ---------- math_tutor ----------
# The solution to the equation `3x + 11 = 14` is `x = 1`.
# 2025-02-09 13:53:46,881 - INFO - HTTP Request: DELETE https://api.openai.com/v1/assistants/asst_Fv9ymRsOlqUdNpJSktOZMg7G "HTTP/1.1 200 OK"
# 2025-02-09 13:53:46,883 - INFO - Example completed successfully
# ```


from openai import AsyncOpenAI
from autogen_core import CancellationToken
import asyncio
from autogen_ext.agents.openai import OpenAIAssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.ui import Console
import logging
import dotenv
import json

from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import  TextMentionTermination

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('assistant_api.log')
    ]
)
logger = logging.getLogger(__name__)

# Import shared environment utilities
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..')))
from shared.utils.env import load_env

# Load environment variables from both root and local .env files
logger.info("Loading environment variables")
load_env()

async def example():
    try:
        logger.info("Starting example")
        cancellation_token = CancellationToken()

        # Create an OpenAI client
        client = AsyncOpenAI()

        # Create an assistant with code interpreter
        logger.info("Creating math tutor assistant")
        assistant = OpenAIAssistantAgent(
            name="math_tutor",
            description="Helps with math questions as a personal Python math tutor",
            client=client,
            model="gpt-4",
            instructions="You are a personal math tutor. Write and run code to answer math questions.",
            tools=["code_interpreter"],
        )

        # Create manual config
        assistant_config = {
            "name": "math_tutor",
            "description": "Helps with math questions as a personal Python math tutor",
            "model": "gpt-4",
            "instructions": "You are a personal math tutor. Write and run code to answer math questions.",
            "tools": ["code_interpreter"],
            "type": "openai_assistant"
        }

        # Save to JSON file
        with open("assistant_config.json", "w") as f:
            json.dump(assistant_config, f, indent=2)

        # Get streaming response from the assistant
        test_question = "I need to solve the equation `3x + 11 = 14`. Can you help me?"
        logger.info(f"Asking question: {test_question}")
        
        # Use Console UI to display streaming response
        await Console(
            assistant.on_messages_stream(
                [TextMessage(source="user", content=test_question)],
                cancellation_token
            )
        )

        # Clean up resources
        await assistant.delete_assistant(cancellation_token)

    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    try:
        asyncio.run(example())
        logger.info("Example completed successfully")
    except Exception as e:
        logger.error(f"Program failed: {str(e)}")
        raise