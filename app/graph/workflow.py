from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.messages import HumanMessage
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.agents.agents import rag_agent, order_agent, refund_agent, ticket_agent

# Define workflow graph
workflow = StateGraph(MessagesState)

# Add agent nodes (no supervisor node needed)
workflow.add_node("rag_agent", rag_agent)
workflow.add_node("order_agent", order_agent)
workflow.add_node("refund_agent", refund_agent)
workflow.add_node("ticket_agent", ticket_agent)

# Routing function - called directly from START
def route_to_agent(state):
    """Route from START to appropriate agent based on intent"""
    messages = state["messages"]
    last_message = messages[-1].content.lower()
    
    if any(word in last_message for word in ["order", "track", "ord", "delivery", "shipped"]):
        return "order_agent"
    elif any(word in last_message for word in ["refund", "return", "exchange", "damaged", "wrong"]):
        return "refund_agent"
    elif any(word in last_message for word in ["policy", "shipping", "faq", "how long", "what is"]):
        return "rag_agent"
    elif any(word in last_message for word in ["payment", "account", "login", "escalate", "complaint"]):
        return "ticket_agent"
    else:
        return "rag_agent"

# Add conditional edges from START
workflow.add_conditional_edges(
    START,
    route_to_agent,
    {
        "rag_agent": "rag_agent",
        "order_agent": "order_agent",
        "refund_agent": "refund_agent",
        "ticket_agent": "ticket_agent"
    }
)

# All agents return to END
workflow.add_edge("rag_agent", END)
workflow.add_edge("order_agent", END)
workflow.add_edge("refund_agent", END)
workflow.add_edge("ticket_agent", END)

# Compile graph
app = workflow.compile()

# Test function
def run_query(user_message: str):
    """Run a query through the workflow"""
    result = app.invoke({"messages": [HumanMessage(content=user_message)]})
    return result["messages"][-1].content
