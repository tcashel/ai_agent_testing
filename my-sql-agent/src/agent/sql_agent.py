"""
SQL query generation and execution agent using LangChain patterns.
"""
from typing import Optional, Dict, List, Any, Union
from typing_extensions import Annotated, TypedDict
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.language_models import BaseLanguageModel
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain import hub
from datetime import datetime

from ..db.config import engine
from ..config.llm_config import LLMConfig

SQL_AGENT_SYSTEM_PROMPT = """You are a helpful SQL assistant that translates natural language questions into SQL queries.

Follow these rules:
1. ONLY return the SQL query, nothing else
2. Use proper SQL syntax and formatting
3. Only use SELECT statements for safety
4. Use meaningful column aliases for readability
5. Include proper JOIN conditions when joining tables
6. Use parameterized queries when filtering dates or strings
7. Add comments to explain complex parts of the query

Example:
Question: "Show me total sales by product category for 2023"
Answer:
SELECT 
    p.category,
    SUM(s.amount) as total_sales
FROM sales s
JOIN products p ON p.id = s.product_id
WHERE EXTRACT(YEAR FROM s.sale_date) = 2023
GROUP BY p.category
ORDER BY total_sales DESC;
"""

class QueryOutput(TypedDict):
    """Output format for SQL query generation."""
    query: Annotated[str, "Syntactically valid SQL query that starts with SELECT"]
    parameters: Annotated[List[Any], "List of parameters for the query"]

class SQLQueryAgent:
    """Agent for translating natural language to SQL queries."""
    
    def __init__(self, llm: BaseLanguageModel | LLMConfig, db: SQLDatabase):
        """Initialize the agent.
        
        Args:
            llm: Language model to use
            db: Database to query
        """
        if isinstance(llm, LLMConfig):
            self.llm = ChatOpenAI(
                model=llm.settings.model_name,
                temperature=llm.settings.temperature,
                api_key=llm.settings.api_key,
                model_kwargs={
                    "functions": [{
                        "name": "generate_sql",
                        "description": "Generate a SQL query from natural language",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "The SQL query to execute"
                                },
                                "parameters": {
                                    "type": "object",
                                    "description": "Query parameters"
                                }
                            },
                            "required": ["query"]
                        }
                    }],
                    "function_call": {"name": "generate_sql"}
                }
            )
        else:
            self.llm = llm
            
        self.db = db
        
    def get_table_info(self) -> str:
        """Get information about tables in the database."""
        return self.db.get_table_info()
        
    async def run(self, query_text: str) -> List[Dict[str, Any]]:
        """Run a natural language query against the database."""
        # First check if the input query contains any unsafe keywords
        query_upper = query_text.upper()
        if any(keyword in query_upper for keyword in 
            ["INSERT", "UPDATE", "DELETE", "DROP", "CREATE", "ALTER", "TRUNCATE"]
        ):
            raise ValueError("Only SELECT queries are allowed")
            
        # Get table info for context
        table_info = self.get_table_info()

        # Create messages for the chat
        messages = [
            SystemMessage(content=SQL_AGENT_SYSTEM_PROMPT),
            HumanMessage(content=f"""
            Given the following SQL tables:
            {table_info}
            
            Create a SQL query to answer this question: {query_text}
            """)
        ]

        # Get response from LLM
        response = await self.llm.ainvoke(messages)
        print(f"LLM Response: {response}")  # Debug logging
        
        # Extract query from function call response
        if hasattr(response, "additional_kwargs") and "function_call" in response.additional_kwargs:
            # Parse function call response
            function_args = eval(response.additional_kwargs["function_call"]["arguments"])
            query = function_args["query"]
            parameters = function_args.get("parameters", {})
        else:
            # Fallback to direct response
            query = response.content
            parameters = {}

        # Validate generated query is SELECT only
        if not query.strip().upper().startswith("SELECT"):
            raise ValueError("Only SELECT queries are allowed")

        # Execute query
        result = self.db._execute(
            command=query,
            parameters=parameters,
            fetch="all"
        )
        
        # Convert datetime objects to ISO format strings for consistent comparison
        for row in result:
            for key, value in row.items():
                if isinstance(value, datetime):
                    row[key] = value.isoformat()
                    
        return result