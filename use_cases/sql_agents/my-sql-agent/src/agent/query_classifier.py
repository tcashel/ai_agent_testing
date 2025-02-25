"""
Query planning module to determine the sequence of operations needed for a query.
"""
from enum import Enum
from typing import List, Optional, Dict, Literal
from pydantic import BaseModel, Field, ConfigDict

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

from ..config.llm_config import LLMConfig, create_llm, OpenAISettings

class OperationType(str, Enum):
    """Types of operations that can be performed on data."""
    DATA_RETRIEVAL = "data_retrieval"
    DATA_ANALYSIS = "data_analysis"
    DATA_VISUALIZATION = "data_visualization"
    UNKNOWN = "unknown"

class QueryStep(BaseModel):
    """A single step in a query execution plan."""
    model_config = ConfigDict(extra='forbid')
    
    operation_type: OperationType = Field(
        description="The type of operation to perform"
    )
    description: str = Field(
        description="A brief description of what needs to be done"
    )
    required_fields: Optional[List[str]] = Field(
        default=None,
        description="List of required data fields"
    )

class QueryPlan(BaseModel):
    """Complete execution plan for a query including all required operations."""
    model_config = ConfigDict(extra='forbid')
    
    primary_operation: OperationType = Field(
        description="The main operation type for this query"
    )
    operations: List[QueryStep] = Field(
        description="Ordered list of steps needed"
    )

def create_planner_prompt() -> ChatPromptTemplate:
    """Create the prompt template for query planning."""
    system_message = """You are a query planner that classifies and breaks down data operations into steps.

CRITICAL: You MUST follow these rules EXACTLY for operation type selection:

1. IF query STARTS WITH any of these words:
   - "show"
   - "get"
   - "fetch"
   - "list"
   - "display"
   THEN primary_operation MUST BE "data_retrieval"
   Example: "Get sales data" -> primary_operation: "data_retrieval"

2. IF query CONTAINS any of these words:
   - "average"
   - "mean"
   - "sum"
   - "total"
   - "calculate"
   THEN primary_operation MUST BE "data_analysis"
   Example: "What is the average" -> primary_operation: "data_analysis"

3. IF query CONTAINS any of these words:
   - "chart"
   - "plot"
   - "graph"
   - "visualize"
   THEN primary_operation MUST BE "data_visualization"
   Example: "Create a chart" -> primary_operation: "data_visualization"

CRITICAL: You MUST follow these rules EXACTLY for required fields:
1. For sales data: MUST use "sales_amount" (never "amount" or "sales")
2. For customer data: MUST use "customer_id" (never "id" or "customer")
3. For revenue data: MUST use "revenue" (never "earnings" or "income")
4. For dates: MUST use "date" (never "time" or "period")

CRITICAL: You MUST follow these rules EXACTLY for step sequences:
1. For data_retrieval:
   - EXACTLY ONE step
   - Step MUST be type: "data_retrieval"

2. For data_analysis:
   - EXACTLY TWO steps in this order:
     Step 1: type "data_retrieval"
     Step 2: type "data_analysis"

3. For data_visualization:
   - EXACTLY TWO steps in this order:
     Step 1: type "data_retrieval"
     Step 2: type "data_visualization"

Analyze this query following the above rules EXACTLY: {query}"""
    
    return ChatPromptTemplate.from_messages([
        SystemMessage(content=system_message)
    ])

class QueryPlanner:
    """Plans the execution of natural language queries by breaking them into ordered steps."""

    def __init__(self, config: Optional[LLMConfig] = None):
        """Initialize the planner with a language model.
        
        Args:
            config: Optional LLM configuration. If not provided, loads from environment.
        """
        self.config = config or LLMConfig.from_env()
        
        # Define the function schema for query planning
        self.planning_function = {
            "name": "plan_query",
            "description": "Plan the execution of a data query following strict rules",
            "parameters": {
                "type": "object",
                "properties": {
                    "primary_operation": {
                        "type": "string",
                        "enum": ["data_retrieval", "data_analysis", "data_visualization"],
                        "description": """CRITICAL: You MUST select the operation type following these rules EXACTLY:
1. IF query STARTS WITH: show, get, fetch, list, display -> MUST BE "data_retrieval"
2. IF query CONTAINS: average, mean, sum, total, calculate -> MUST BE "data_analysis"
3. IF query CONTAINS: chart, plot, graph, visualize -> MUST BE "data_visualization"
"""
                    },
                    "operations": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "operation_type": {
                                    "type": "string",
                                    "enum": ["data_retrieval", "data_analysis", "data_visualization"],
                                    "description": """CRITICAL: Operation type MUST follow these rules:
1. For data_retrieval primary: EXACTLY ONE step of type data_retrieval
2. For data_analysis primary: TWO steps - FIRST data_retrieval, SECOND data_analysis
3. For data_visualization primary: TWO steps - FIRST data_retrieval, SECOND data_visualization"""
                                },
                                "description": {
                                    "type": "string",
                                    "description": "A brief description of what needs to be done"
                                },
                                "required_fields": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": """CRITICAL: Field names MUST follow these rules:
1. For sales data: MUST use "sales_amount" (never amount/sales)
2. For customer data: MUST use "customer_id" (never id/customer)
3. For revenue data: MUST use "revenue" (never earnings/income)
4. For dates: MUST use "date" (never time/period)"""
                                }
                            },
                            "required": ["operation_type", "description", "required_fields"]
                        },
                        "minItems": 1,
                        "maxItems": 2
                    }
                },
                "required": ["primary_operation", "operations"]
            }
        }
        
        # Create LLM with function calling
        if isinstance(self.config.settings, OpenAISettings):
            self.llm = ChatOpenAI(
                model_name=self.config.settings.model_name,
                temperature=0.0,  # Force deterministic output
                openai_api_key=self.config.settings.api_key,
                model_kwargs={
                    "functions": [self.planning_function],
                    "function_call": {"name": "plan_query"}
                }
            )
        else:
            # Fallback to regular LLM for non-OpenAI models
            self.llm = create_llm(self.config)
        
        # Create planning chain
        self.prompt = create_planner_prompt()
        self.chain = self.prompt | self.llm
    
    def _parse_response(self, response: str) -> QueryPlan:
        """Parse the LLM response into a QueryPlan.
        
        Args:
            response: Raw response from the LLM
            
        Returns:
            QueryPlan: Structured plan from the response
        """
        try:
            # Split into type and steps
            type_line, steps_section = response.split("STEPS:", 1)
            
            # Clean up the operation type and convert to lowercase
            primary_op = type_line.split("TYPE:", 1)[1].strip().lower()
            # Remove any trailing newlines or whitespace
            primary_op = primary_op.rstrip('\\n').strip()
            
            # Parse steps
            operations = []
            for step in steps_section.strip().split("\n"):
                if not step.strip():
                    continue
                    
                # Parse step format: "1. operation: <type> - <description> - fields: [<fields>]"
                parts = step.split(" - ", 2)
                if len(parts) != 3:
                    continue
                    
                # Clean up the operation type
                op_type = parts[0].split(": ")[1].strip().lower()
                # Remove any trailing newlines or whitespace
                op_type = op_type.rstrip('\\n').strip()
                
                description = parts[1].strip()
                # Clean up the fields list
                fields_str = parts[2].split("fields: ")[1].strip("[]").strip()
                fields = [f.strip() for f in fields_str.split(",")] if fields_str else None
                
                try:
                    operations.append(QueryStep(
                        operation_type=OperationType(op_type),
                        description=description,
                        required_fields=fields
                    ))
                except ValueError:
                    print(f"Invalid operation type: {op_type}")
                    continue
            
            try:
                return QueryPlan(
                    primary_operation=OperationType(primary_op),
                    operations=operations
                )
            except ValueError:
                print(f"Invalid primary operation type: {primary_op}")
                return QueryPlan(
                    primary_operation=OperationType.UNKNOWN,
                    operations=operations
                )
                
        except Exception as e:
            print(f"Error parsing response: {str(e)}")
            print(f"Raw response: {response}")
            return QueryPlan(
                primary_operation=OperationType.UNKNOWN,
                operations=[
                    QueryStep(
                        operation_type=OperationType.UNKNOWN,
                        description="Could not parse response"
                    )
                ]
            )
    
    async def plan(self, query: str) -> QueryPlan:
        """Create an execution plan for a natural language query.
        
        Args:
            query: The user's natural language query
            
        Returns:
            QueryPlan: Complete execution plan for the query
        """
        try:
            # Get response from LLM
            response = await self.chain.ainvoke({"query": query})
            
            if hasattr(response, "additional_kwargs") and "function_call" in response.additional_kwargs:
                # Parse function call response
                result = response.additional_kwargs["function_call"]["arguments"]
                return QueryPlan.model_validate_json(result)
            else:
                # Fallback to text parsing for non-OpenAI models
                return self._parse_response(str(response))
                
        except Exception as e:
            print(f"Error planning query: {str(e)}")
            return QueryPlan(
                primary_operation=OperationType.UNKNOWN,
                operations=[
                    QueryStep(
                        operation_type=OperationType.UNKNOWN,
                        description="Could not plan query due to error"
                    )
                ]
            ) 