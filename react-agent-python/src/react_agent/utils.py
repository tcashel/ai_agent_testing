"""Utility & helper functions."""

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage


def get_message_text(msg: BaseMessage) -> str:
    """Get the text content of a message."""
    content = msg.content
    if isinstance(content, str):
        return content
    elif isinstance(content, dict):
        return content.get("text", "")
    else:
        txts = [c if isinstance(c, str) else (c.get("text") or "") for c in content]
        return "".join(txts).strip()


def load_chat_model(fully_specified_name: str) -> BaseChatModel:
    """Load a chat model from a fully specified name.

    Args:
        fully_specified_name (str): String in the format 'provider/model'.
            Example: 'anthropic/claude-3-sonnet-20240229' or 'openai/gpt-4-turbo-preview'

    Returns:
        BaseChatModel: Initialized chat model instance.
    """
    provider, model = fully_specified_name.split("/", maxsplit=1)
    return init_chat_model(
        model,
        model_provider=provider,
        # Configure any additional model parameters here
        streaming=True,  # Enable streaming for better UX
        verbose=True,  # Enable verbose mode for debugging
    )
