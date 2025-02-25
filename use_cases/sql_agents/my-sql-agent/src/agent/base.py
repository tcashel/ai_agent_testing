"""
Base agent implementation for handling queries.
"""
from typing import Dict, Optional, Tuple

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate

from .query_classifier import QueryPlanner, OperationType
from ..config.llm_config import LLMConfig, create_llm

class QueryAgent:
    """Basic agent for processing natural language queries."""
    
    def __init__(self, config: Optional[LLMConfig] = None):
        """Initialize the agent with a language model.
        
        Args:
            config: Optional LLM configuration. If not provided, loads from environment.
        """
        self.config = config or LLMConfig.from_env()
        self.planner = QueryPlanner(config=self.config)
        self.llm = create_llm(self.config)
        
        # Create a chat prompt template with clear system and human messages
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are a data operations assistant that provides detailed implementation instructions.

CONTEXT:
For the query: "{query}"
Primary Operation: {primary_operation}
Required Steps:
{operations}

YOUR TASK:
Provide specific, copy-pasteable code for each operation, following these guidelines:

1. DATA_RETRIEVAL Operations:
   - Write exact SQL or pandas commands
   - Include all necessary table names and joins
   - Specify precise filters and conditions
   Example: 
   ```python
   df = pd.read_sql('''
       SELECT date, sales_amount 
       FROM sales 
       WHERE date >= DATE_SUB(NOW(), INTERVAL 1 MONTH)
   ''', conn)
   ```

2. DATA_ANALYSIS Operations:
   - Write exact pandas/numpy calculations
   - Include all grouping and aggregation logic
   - Show intermediate steps if needed
   Example:
   ```python
   avg_revenue = df.groupby('customer_id')['revenue'].agg({
       'mean_revenue': 'mean',
       'total_revenue': 'sum'
   })
   ```

3. DATA_VISUALIZATION Operations:
   - Write complete plotting commands
   - Include figure setup and styling
   - Specify all labels and formatting
   Example:
   ```python
   plt.figure(figsize=(10, 6))
   sns.barplot(data=df, x='date', y='sales_amount')
   plt.title('Monthly Sales')
   plt.xlabel('Date')
   plt.ylabel('Sales Amount')
   ```

RESPONSE FORMAT:
For each operation, provide:
1. A brief description of what the code does
2. The complete, runnable code block
3. Any important notes about dependencies or assumptions"""),
            HumanMessage(content="Please provide the implementation details for each operation.")
        ])
        
        # Create the response chain
        self.chain = self.prompt | self.llm
    
    async def process_query(self, query: str) -> str:
        """Process a natural language query.
        
        Args:
            query: The user's natural language query
            
        Returns:
            str: The agent's response
        """
        try:
            # First plan the query operations
            plan = await self.planner.plan(query)
            
            # Process the query with knowledge of all required operations
            response = await self.chain.ainvoke({
                "query": query,
                "primary_operation": plan.primary_operation.value.upper(),
                "operations": "\n".join(f"- {op.operation_type.value.upper()}: {op.description}" 
                                      for op in plan.operations)
            })
            return str(response).strip()
        except Exception as e:
            print(f"Error processing query: {str(e)}")
            return f"Error processing query: {str(e)}" 