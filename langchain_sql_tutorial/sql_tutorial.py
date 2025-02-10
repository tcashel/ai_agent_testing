"""
Example implementation of LangChain SQL Question/Answering system.
Based on: https://python.langchain.com/docs/tutorials/sql_qa/
"""
import os
import logging
from typing import List, Dict, Any
from typing_extensions import TypedDict
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph, END
import openlit

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Disable LangSmith warnings
os.environ["LANGCHAIN_TRACING_V2"] = "false"

# Initialize OpenLit with minimal configuration
logger.info("Initializing OpenLit...")
openlit.init(
    otlp_endpoint="http://127.0.0.1:4318",
    application_name="sql-tutorial",
    trace_content=True  # Enable content tracing for debugging
)

# Load environment variables
ENV_PATH = "/Users/tcashel/repositories/ai_agent_testing/my-sql-agent/.env"
logger.info(f"Loading environment variables from: {os.path.abspath(ENV_PATH)}")
load_dotenv(dotenv_path=ENV_PATH)

@openlit.trace
def create_db():
    """Create database connection."""
    logger.debug("Creating database connection...")
    db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    db = SQLDatabase.from_uri(db_url, sample_rows_in_table_info=3)
    logger.debug("Database connection created successfully")
    return db

@openlit.trace
def create_llm():
    """Create and configure the LLM with proper tracing setup."""
    logger.debug("Creating LLM instance...")
    try:
        llm = ChatOpenAI(
            model_name="gpt-4-turbo-preview",
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY"),
            verbose=True
        )
        logger.debug("LLM created successfully")
        return llm
    except Exception as e:
        logger.error(f"Error creating LLM: {str(e)}")
        raise

@openlit.trace
def main():
    """Run example queries against our database."""
    try:
        # Initialize components
        db = create_db()
        llm = create_llm()
        
        logger.debug("Creating SQL toolkit...")
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        tools = toolkit.get_tools()
        logger.debug(f"Created {len(tools)} tools")
        
        logger.debug("Loading system prompt...")
        system_message = hub.pull("langchain-ai/sql-agent-system-prompt").format(
            dialect="PostgreSQL",
            top_k=3
        )
        
        logger.debug("Creating ReAct agent...")
        agent_executor = create_react_agent(llm, tools, prompt=system_message)
        
        questions = [
            "Which customers spent the most?",
        ]
        
        for question in questions:
            with openlit.start_trace(name="process_question") as trace:
                logger.info(f"\nProcessing question: {question}")
                messages = [{"role": "user", "content": question}]
                trace.set_metadata({"question": question})
                
                try:
                    # Stream the agent's steps with proper message handling
                    for step in agent_executor.stream({"messages": messages}):
                        if "messages" in step and step["messages"]:
                            last_message = step["messages"][-1]
                            if hasattr(last_message, "pretty_print"):
                                last_message.pretty_print()
                                trace.set_metadata({"response_type": "pretty_print"})
                            else:
                                print(f"{last_message.type}: {last_message.content}")
                                trace.set_metadata({
                                    "response_type": "text",
                                    "message_type": last_message.type
                                })
                            
                            # Set the result in the trace
                            if hasattr(last_message, "content"):
                                trace.set_result(last_message.content)
                                
                except Exception as e:
                    logger.error(f"Error processing question: {str(e)}", exc_info=True)
                    trace.set_result(f"Error: {str(e)}")
                    openlit.log_error(e)
                    
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}", exc_info=True)
        openlit.log_error(e)

if __name__ == "__main__":
    main() 