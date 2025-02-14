"""Code generation and execution tools for the React Agent."""
from typing import List, Optional
from langchain_core.tools import BaseTool

# Set matplotlib backend before importing pyplot
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

from langchain_experimental.tools import PythonAstREPLTool
from langchain_experimental.tools.python.tool import PythonREPLTool

from react_agent.configuration import Configuration


def get_code_tools(config: Optional[Configuration] = None) -> List[BaseTool]:
    """Get code tools with configuration.
    
    Args:
        config: Optional configuration instance. If None, uses default configuration.
        
    Returns:
        List of Python REPL tools for code execution.
    """
    if config is None:
        config = Configuration()
        
    # Use Langchain's built-in Python REPL tools
    python_repl = PythonREPLTool()
    python_ast_repl = PythonAstREPLTool(
        timeout=config.code_execution_timeout,
        globals={"config": config},  # Pass configuration to the tool
    )
    
    return [python_repl, python_ast_repl] 