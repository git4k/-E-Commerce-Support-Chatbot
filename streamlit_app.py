import streamlit as st
from langchain_core.messages import HumanMessage
import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).parent))
from app.graph.workflow import app as workflow_app

st.set_page_config(page_title="E-Commerce AI Support", page_icon="🛒")
st.title("🛒 E-Commerce AI Support")
st.caption("Multi-Agent Customer Support System")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about orders, refunds, or policies..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        status = st.empty()
        status.info("🤔 Analyzing your question...")
        
        try:
            start_time = time.time()
            result = workflow_app.invoke({"messages": [HumanMessage(content=prompt)]})
            elapsed = time.time() - start_time
            
            response = result["messages"][-1].content
            status.empty()
            st.markdown(response)
            st.caption(f"⚡ Response time: {elapsed:.2f}s")
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            status.empty()
            error_msg = f"Error: {str(e)}"
            st.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Sidebar with examples
with st.sidebar:
    st.header("Example Queries")
    st.markdown("""
    **Order Status:**
    - Where is my order ORD101?
    - Track order ORD150
    
    **Refunds:**
    - I want to return order ORD120
    - My item arrived damaged
    
    **Policies:**
    - What is your return policy?
    - How long does shipping take?
    
    **Support:**
    - My payment failed
    - I can't log into my account
    """)
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.caption("💡 First query may be slower (loading models)")
    st.caption("⚡ Powered by Groq + Llama 3.1")
