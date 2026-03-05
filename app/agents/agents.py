from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config import llm
from app.tools.tools import check_order_status, create_refund, create_support_ticket, search_policy_docs

# Create agents (optimized with faster LLM)
rag_agent = create_react_agent(llm, tools=[search_policy_docs])
order_agent = create_react_agent(llm, tools=[check_order_status])
refund_agent = create_react_agent(llm, tools=[create_refund, search_policy_docs])
ticket_agent = create_react_agent(llm, tools=[create_support_ticket])
