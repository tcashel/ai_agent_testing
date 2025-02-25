# Prompt Guarding Tools

This project provides examples of implementing prompt guards and content moderation with different LLM providers.

## Features

- OpenAI Moderation API implementation
- Llama Guard prompt classification
- Content safety filtering techniques
- Integration with OpenLit for observability

## Setup

1. Install dependencies:
```bash
# Install with Poetry
poetry install

# Activate the environment
poetry shell
```

2. Make sure your API keys are set in the project's `.env` file.

## Usage

- `llama-guard-3-testing.py`: Example using Llama Guard for prompt classification
- `openAI-moderation-testing.py`: Example using OpenAI's Moderation API

## How It Works

These tools help detect harmful, inappropriate, or sensitive content in user inputs before they reach your main LLM. They can:

1. Classify user inputs into safety categories
2. Flag potential harmful content for review
3. Provide explanations for moderation decisions
4. Integrate with your existing agent workflows