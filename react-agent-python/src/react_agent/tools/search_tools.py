"""Search tools for the agent."""
from typing import Any, Optional, Dict
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import InjectedToolArg
from typing_extensions import Annotated

async def search(
    query: str, *, config: Annotated[RunnableConfig, InjectedToolArg]
) -> Optional[list[dict[str, Any]]]:
    """Search for general web results using Tavily search engine."""
    wrapped = TavilySearchResults(max_results=10)
    result = await wrapped.ainvoke({"query": query})
    return result 