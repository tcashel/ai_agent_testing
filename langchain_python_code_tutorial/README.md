# LangChain Python Code Executor

A simple example demonstrating how to use LangChain to create an AI agent that can write and execute Python code safely.

⚠️ **Security Warning**: The Python REPL executes code locally on your machine. It can execute arbitrary code (e.g., delete files, make network requests). Use with caution and only run code you trust.

## Setup

1. Install dependencies:
```bash
pip install langchain langchain-openai langchain-experimental python-dotenv
```

2. Set up your environment variables in a `.env` file:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

Run the example:
```bash
python python_runner.py
```

## Example Output

```
Question: Calculate the first 10 Fibonacci numbers
--------------------------------------------------
The first 10 Fibonacci numbers are: 0, 1, 1, 2, 3, 5, 8, 13, 21, and 34.
--------------------------------------------------

Question: Create a list of the first 5 prime numbers and multiply them together
--------------------------------------------------
The first 5 prime numbers are 2, 3, 5, 7, and 11. When multiplied together, their product is 2310.
--------------------------------------------------

Question: Generate a simple bar chart of the numbers [1, 4, 2, 7, 5] using ASCII characters
--------------------------------------------------
The simple bar chart of the numbers [1, 4, 2, 7, 5] using ASCII characters is shown below:

|*
|****
|**
|*******
|*****
---------
```

## Features

- Local Python code execution using LangChain's experimental REPL
- GPT-4 powered code generation
- Example tasks including:
  - Mathematical calculations
  - Data manipulation
  - ASCII visualization

## Security Considerations

This tool uses LangChain's experimental Python REPL which:
- Executes code directly on your local machine
- Can perform any operation your Python environment has access to
- Should only be used with trusted input and in controlled environments
- For more information on security, see [LangChain's security guidelines](https://python.langchain.com/docs/security/) 