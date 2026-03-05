"""Simplified version without agents - direct tool calls"""
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).parent))
from config import llm
from app.tools.tools import check_order_status, create_refund, create_support_ticket, search_policy_docs

st.set_page_config(page_title="E-Commerce AI Support", page_icon="🛒")
st.title("🛒 E-Commerce AI Support")
st.caption("Multi-Agent Customer Support System ")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def route_and_respond(user_message: str) -> str:
    """Simple routing without agents"""
    msg_lower = user_message.lower()
    
    # Route based on keywords
    if any(word in msg_lower for word in ["order", "track", "ord", "delivery", "shipped"]):
        # Extract order ID
        import re
        order_match = re.search(r'ord\d+', msg_lower)
        if order_match:
            order_id = order_match.group(0).upper()
            result = check_order_status.invoke(order_id)
            return f"Let me check that for you.\n\n{result}"
        return "Please provide your order ID (e.g., ORD101) so I can track it for you."
    
    elif any(word in msg_lower for word in ["refund", "return", "exchange", "damaged"]):
        # Check if order ID mentioned
        import re
        order_match = re.search(r'ord\d+', msg_lower)
        if order_match:
            order_id = order_match.group(0).upper()
            result = create_refund.invoke(order_id)
            return f"I'll help you with that return.\n\n{result}"
        return "I can help you with a return. Please provide your order ID (e.g., ORD101)."
    
    elif any(word in msg_lower for word in ["policy", "shipping", "faq", "how long", "what is"]):
        # RAG search
        result = search_policy_docs.invoke(user_message)
        # Use LLM to format the answer
        prompt = f"Based on this policy information:\n\n{result}\n\nAnswer the customer's question: {user_message}\n\nBe concise and helpful."
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content
    
    elif any(word in msg_lower for word in ["payment", "account", "login", "help", "support"]):
        result = create_support_ticket.invoke({"customer_id": 1, "issue_type": "general", "description": user_message})
        return f"I'll escalate this to our support team.\n\n{result}"
    
    else:
        # Default to RAG
        result = search_policy_docs.invoke(user_message)
        prompt = f"Based on this information:\n\n{result}\n\nAnswer: {user_message}\n\nBe helpful and concise."
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content

# Chat input
if prompt := st.chat_input("Ask about orders, refunds, or policies..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        status = st.empty()
        status.info("🤔 Processing...")
        
        try:
            start_time = time.time()
            response = route_and_respond(prompt)
            elapsed = time.time() - start_time
            
            status.empty()
            st.markdown(response)
            st.caption(f"⚡ Response time: {elapsed:.2f}s")
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            status.empty()
            error_msg = f"Error: {str(e)}"
            st.error(error_msg)
            import traceback
            st.code(traceback.format_exc())
            st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Sidebar
with st.sidebar:
    st.header("Example Queries")
    st.markdown("""
    **Order Status:**
    - Where is my order ORD101?
    
    **Refunds:**
    - I want to return order ORD120
    
    **Policies:**
    - What is your return policy?
    
    **Support:**
    - My payment failed
    """)
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.caption("⚡KB")
