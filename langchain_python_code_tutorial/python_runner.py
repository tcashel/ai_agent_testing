"""
Example implementation of using LangChain's PythonAstREPLTool to safely execute Python code.
"""
from typing import List
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_experimental.utilities import PythonREPL
from langchain_core.tools import Tool
from langchain import hub
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
import os

# Load environment variables (for API keys)
ENV_PATH = "/Users/tcashel/repositories/ai_agent_testing/my-sql-agent/.env"
load_dotenv(dotenv_path=ENV_PATH)

def create_python_executor():
    """Create a LangChain agent that can execute Python code safely."""
    
    # Initialize the Python REPL
    python_repl = PythonREPL()
    
    # Create the Python REPL tool with proper description
    python_tool = Tool(
        name="python_repl",
        description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
        func=python_repl.run
    )
    
    # Initialize the language model
    llm = ChatOpenAI(
        model_name="gpt-4-turbo-preview",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create a list of tools
    tools = [python_tool]
    
    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful AI assistant that can write and execute Python code.
        When asked to perform calculations or manipulate data, you should write and execute Python code to accomplish the task.
        Always explain your code and its output clearly.
        Remember to use print() to show the results of your calculations."""),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # Bind the tools to the LLM
    llm_with_tools = llm.bind(
        functions=[convert_to_openai_function(t) for t in tools]
    )
    
    # Create the runnable agent
    runnable_agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_function_messages(
                x["intermediate_steps"]
            ),
        }
        | prompt
        | llm_with_tools
        | OpenAIFunctionsAgentOutputParser()
    )
    
    # Create the agent executor
    agent_executor = AgentExecutor(
        agent=runnable_agent,
        tools=tools,
        handle_parsing_errors=True
    )
    
    return agent_executor

def main():
    """Run example Python code execution tasks."""
    agent = create_python_executor()
    
    # Example questions that require Python code execution
    questions = [
        "Calculate the first 10 Fibonacci numbers",
        "Create a list of the first 5 prime numbers and multiply them together",
        "Generate a simple bar chart of the numbers [1, 4, 2, 7, 5] using ASCII characters"
    ]
    
    for question in questions:
        print(f"\nQuestion: {question}")
        print("-" * 50)
        
        try:
            # Execute the agent
            result = agent.invoke({"input": question})
            print(result["output"])
        except Exception as e:
            print(f"Error: {str(e)}")
        
        print("-" * 50)

if __name__ == "__main__":
    main()
